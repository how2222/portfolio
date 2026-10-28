# Project portfolio — how to use

## Install
1. Quarto: https://quarto.org/docs/get-started/ (Typst is bundled, no LaTeX needed).
2. `git init` in this folder, then push to GitHub (`how2222/portfolio`).
3. URLs in `_quarto.yml` and CV PDFs in `cv/` are already set.

## Write a project sheet
1. `cp projects/_template.qmd projects/<slug>.qmd`
2. Fill in the YAML, then the sections. The `<!-- comments -->` are the guidance; delete them once a section is written.
3. One image `assets/<slug>/cover.jpg` (16:9) and one diagram `assets/<slug>/architecture.png`.
4. `quarto preview` to see the result live.

Structure enforced on every sheet:
Pitch → Context → Technical problem → Approach & architecture (diagram + decision table) → My contribution → Results → Limits → Links → Interview Q&A (private).

## Build the outputs
| Need | Command | Output |
|---|---|---|
| Full site + PDF of every sheet | `quarto render` | `_site/` |
| Private version with the Q&A | `quarto render --profile prep` | `_prep/` (never publish) |
| PDF of a single sheet | `quarto render projects/drone.qmd --to typst` | `projects/drone.pdf` |
| Deploy | `quarto publish gh-pages` | GitHub Pages |

## For an application
- Link to the site in the CV and the email.
- Attach the PDF of the most relevant sheet for the role (1 page).
- Re-read the sheet's Q&A section (`prep` profile) the day before the interview.
