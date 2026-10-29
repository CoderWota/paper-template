-- Bring Pandoc's reading of an editable manuscript (Word, OpenDocument, or LaTeX) to the workspace's
-- Markdown conventions (docs/markdown-and-export-conventions.md):
--   * a display formula stands on its own lines between $$ lines, and its label follows as a separate
--     "{#eq:id}" paragraph after a blank line, because GitHub stops rendering a formula with text on its
--     closing line; LaTeX equation environments, \label, \nonumber, and \notag are unwrapped or removed;
--   * labels carry the cross-reference prefixes fig:, tbl:, eq:, and sec:, learned in a first pass from
--     where each label is defined, so that \ref{x} and \eqref{x} become @fig:x, @eq:x, and so on;
--   * a formula inside running text from an OpenDocument file becomes inline again, because Pandoc's
--     OpenDocument reader marks every formula as display math;
--   * LaTeX float placement is dropped.
-- Comments and tracked changes stay as Pandoc marks them, so that the adoption step can stop on them.
-- The metadata field "adopt-source" names the input kind (word, opendocument, latex).

local source = "word"
local kinds = {}

local PREFIXES = {"fig", "figure", "tbl", "tab", "table", "eq", "eqn", "equation", "sec", "section", "subsec", "chap", "ch"}

local function bare(label)
  for _, prefix in ipairs(PREFIXES) do
    local rest = label:match("^" .. prefix .. "[:%-_](.+)$")
    if rest then
      return rest
    end
  end
  return label
end

local function renamed(label)
  local kind = kinds[label]
  if not kind or label == "" then
    return label
  end
  return kind .. ":" .. bare(label)
end

local function equation_label(tex)
  return tex:match("\\label%s*{([^}]*)}")
end

-- Pass 0: read the input kind first, because a filter visits blocks before the metadata.

local read_source = {
  Meta = function(meta)
    if meta["adopt-source"] then
      source = pandoc.utils.stringify(meta["adopt-source"])
    end
  end,
}

-- Pass 1: learn the kind of every label from where it is defined.

local learn = {
  Header = function(header)
    if header.identifier ~= "" and source == "latex" then
      kinds[header.identifier] = "sec"
    end
  end,
  Figure = function(figure)
    if figure.identifier ~= "" then
      kinds[figure.identifier] = "fig"
    end
  end,
  Table = function(table)
    if table.identifier ~= "" then
      kinds[table.identifier] = "tbl"
    end
  end,
  Math = function(math)
    local label = math.mathtype == "DisplayMath" and equation_label(math.text)
    if label then
      kinds[label] = "eq"
    end
  end,
}

-- Pass 2: rewrite formulas, labels, and references.

local function display_blocks(tex)
  local label = equation_label(tex)
  tex = tex:gsub("\\label%s*{[^}]*}", ""):gsub("\\nonumber", ""):gsub("\\notag", "")
  local environment, body = tex:match("^%s*\\begin{(%a+%*?)}(.-)\\end{%a+%*?}%s*$")
  if environment == "equation" or environment == "equation*" or environment == "displaymath" then
    tex = body
  elseif environment == "align" or environment == "align*" or environment == "eqnarray" or environment == "eqnarray*" then
    tex = "\\begin{aligned}" .. body .. "\\end{aligned}"
  elseif environment == "gather" or environment == "gather*" then
    tex = "\\begin{gathered}" .. body .. "\\end{gathered}"
  end
  tex = tex:gsub("^%s+", ""):gsub("%s+$", ""):gsub("\n%s*\n", "\n")
  local text = "$$\n" .. tex .. "\n$$"
  if label then
    text = text .. "\n\n{#" .. renamed(label) .. "}"
  end
  return {pandoc.RawBlock("markdown", text)}
end

local function is_space(inline)
  return inline.t == "Space" or inline.t == "SoftBreak" or inline.t == "LineBreak"
end

local function has_text(inlines)
  for _, inline in ipairs(inlines) do
    if not is_space(inline) and not (inline.t == "Math" and inline.mathtype == "DisplayMath") then
      return true
    end
  end
  return false
end

local function split_paragraph(paragraph)
  local displays = false
  for _, inline in ipairs(paragraph.content) do
    if inline.t == "Math" and inline.mathtype == "DisplayMath" then
      displays = true
    end
  end
  if not displays then
    return nil
  end
  if source == "opendocument" and has_text(paragraph.content) then
    return pandoc.Para(paragraph.content:map(function(inline)
      if inline.t == "Math" and inline.mathtype == "DisplayMath" then
        return pandoc.Math("InlineMath", inline.text)
      end
      return inline
    end))
  end
  local blocks, current = pandoc.List(), pandoc.List()
  local function flush()
    while #current > 0 and is_space(current[#current]) do
      current:remove(#current)
    end
    if #current > 0 then
      blocks:insert(pandoc.Para(current))
    end
    current = pandoc.List()
  end
  for _, inline in ipairs(paragraph.content) do
    if inline.t == "Math" and inline.mathtype == "DisplayMath" then
      flush()
      blocks:extend(display_blocks(inline.text))
    elseif not (#current == 0 and is_space(inline)) then
      current:insert(inline)
    end
  end
  flush()
  return blocks
end

local rewrite = {
  Meta = function(meta)
    meta["adopt-source"] = nil
    return meta
  end,
  Para = split_paragraph,
  Plain = split_paragraph,
  Header = function(header)
    header.identifier = renamed(header.identifier)
    return header
  end,
  Figure = function(figure)
    figure.identifier = renamed(figure.identifier)
    figure.attributes["latex-placement"] = nil
    return figure
  end,
  Table = function(table)
    table.identifier = renamed(table.identifier)
    return table
  end,
  Span = function(span)
    -- An empty span with only an identifier is a bookmark from the word processor; workspace labels replace it.
    if #span.content == 0 and span.identifier ~= "" and #span.classes == 0 then
      return {}
    end
  end,
  Link = function(link)
    local target = link.attributes["reference"]
    if link.attributes["reference-type"] and target then
      local label = renamed(target)
      return pandoc.Cite({pandoc.Str("@" .. label)}, {pandoc.Citation(label, "AuthorInText")})
    end
  end,
}

return {read_source, learn, rewrite}
