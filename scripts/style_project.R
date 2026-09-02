# Run the project's pinned styler configuration.
# Usage: source this file, or Rscript scripts/style_project.R

library(styler)

style_dir(
  path = ".",
  style = tidyverse_style,
  indent_by = 2,
  scope = "tokens"
)
