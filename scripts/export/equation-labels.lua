-- Attach an equation label written as its own paragraph ("{#eq:...}") to the display equation just
-- before it, so that pandoc-crossref sees "$$...$$ {#eq:...}". The workspace writes the label after a
-- blank line because GitHub does not render a display equation that has text on its closing line
-- (docs/export-trial.md). Run this filter before pandoc-crossref.

local function label_of(block)
  if block.t ~= "Para" or #block.content ~= 1 or block.content[1].t ~= "Str" then
    return nil
  end
  local text = block.content[1].text
  if text:match("^{#eq:[^%s{}]+}$") then
    return text
  end
  return nil
end

local function ends_with_display_math(block)
  if block.t ~= "Para" and block.t ~= "Plain" then
    return false
  end
  local last = block.content[#block.content]
  return last ~= nil and last.t == "Math" and last.mathtype == "DisplayMath"
end

function Blocks(blocks)
  local result = pandoc.List()
  local i = 1
  while i <= #blocks do
    local block, following = blocks[i], blocks[i + 1]
    local label = following and label_of(following)
    if label and ends_with_display_math(block) then
      block.content:insert(pandoc.Space())
      block.content:insert(pandoc.Str(label))
      i = i + 2
    else
      i = i + 1
    end
    result:insert(block)
  end
  return result
end
