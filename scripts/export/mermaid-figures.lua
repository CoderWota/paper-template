-- Replace each Mermaid code block with the figure that scripts/export.py rendered for it, and use the
-- caption paragraph after the block (": Caption {#fig:id}") as its caption and label. The rendered image
-- is <figures-dir>/<sha1 of the block text>.png; the folder comes from the metadata field
-- "mermaid-figures". A block without a rendered image is left as code, and a warning names it, so the
-- build reports the diagram as not rendered. Run this filter before pandoc-crossref.

local folder = nil

local function caption_of(block)
  if not block or block.t ~= "Para" then
    return nil
  end
  local text = pandoc.utils.stringify(block)
  local caption, identifier = text:match("^:%s+(.-)%s*{#(fig:[^%s}]+)}%s*$")
  if not caption then
    return nil
  end
  local inlines = pandoc.List(block.content)
  -- Drop the leading ":" and the trailing "{#fig:...}" while keeping the caption's own formatting.
  while #inlines > 0 and (inlines[1].t == "Space" or (inlines[1].t == "Str" and inlines[1].text == ":")) do
    inlines:remove(1)
  end
  while #inlines > 0 and (inlines[#inlines].t == "Space" or (inlines[#inlines].t == "Str" and inlines[#inlines].text:match("{#fig:"))) do
    inlines:remove(#inlines)
  end
  return inlines, identifier
end

local function file_exists(path)
  local handle = io.open(path, "rb")
  if handle then
    handle:close()
    return true
  end
  return false
end

function Meta(meta)
  if meta["mermaid-figures"] then
    folder = pandoc.utils.stringify(meta["mermaid-figures"])
  end
  return meta
end

function Blocks(blocks)
  local result = pandoc.List()
  local i = 1
  while i <= #blocks do
    local block = blocks[i]
    if block.t == "CodeBlock" and block.classes:includes("mermaid") then
      local image = folder and (folder .. "/" .. pandoc.utils.sha1(block.text) .. ".png")
      if image and file_exists(image) then
        local caption, identifier = caption_of(blocks[i + 1])
        local inlines = caption or pandoc.List()
        -- A Figure block, as Pandoc's Markdown reader makes for "![Caption](path){#fig:id}", so that
        -- pandoc-crossref numbers it.
        result:insert(pandoc.Figure({pandoc.Plain({pandoc.Image(inlines, image)})}, {pandoc.Plain(inlines)},
                                    pandoc.Attr(identifier or "", {}, {})))
        i = i + (caption and 2 or 1)
      else
        io.stderr:write("[WARNING] mermaid-figures: a diagram was not rendered; it stays as code\n")
        result:insert(block)
        i = i + 1
      end
    else
      result:insert(block)
      i = i + 1
    end
  end
  return result
end

return {{Meta = Meta}, {Blocks = Blocks}}
