# CCL Website

This repository contains the source code for the Cooperative Computing Lab (CCL) website. The site is built with Jekyll and uses the al-folio theme as a base.

## Deployment

- To deploy and test locally, see [INSTALL.md](INSTALL.md).

## Blogs

Blogging is supported with advanced features (code highlighting, Plotly graphs, image galleries, pseudo code, and more). Users should add posts and assets as follows:

- Put your post in `_posts/<year>/` (example: `_posts/2025/2025-12-03-new-post.md`).
- Put blog images and related assets under `assets/blog/<year>/<slug>/` (example: `assets/blog/2025/new-post/hero.jpg`).
- Reference these assets from your post content using relative paths.

For examples of advanced blogging features, see the [al-folio blog examples](https://alshedivat.github.io/al-folio/blog/).

## People

Lab members can add themselves to the People page:

- Add your photo to `assets/img/people/` (example: `assets/img/people/jane-doe.jpg`).
- Edit `/_pages/people.md` to include your entry and reference your photo.

## Papers

To add a new research paper to the website:

1. **Edit `_bibliography/papers.bib`** and add a new entry with at least the following fields:

```bibtex
@inproceedings {
my-paper-key-2025,
author = "John Doe and Jane Smith",
title = "{My Paper Title}",
booktitle = "{Conference Name}",
year = 2025,
pdf = {my-paper-key-2025.pdf},
preview = {my-paper-key-2025.png},
}
```

Other good to have fields:
- `doi` - Digital Object Identifier (auto-generates link as https://doi.org/{doi})
- `keywords` - Space or comma-separated keywords to categorize papers (e.g., `taskvine`, `workqueue`, `makeflow`, `hep`, `llm`, `gpu`). These keywords can be used to automatically list papers on project pages.

2. **Place files in these directories:**
   - PDF: `assets/paper/pdf/my-paper-key-2025.pdf`
   - Preview: `assets/paper/preview/my-paper-key-2025.png`


**Optional: Auto-generate previews**

If you have the PDF but no preview thumbnail, you can use the script to generate it:
```bash
python script_automation/check_papers.py --generate-missing
```

This can also download PDFs from ArXiv (provide the abstract URL in the `url` field, e.g., `https://arxiv.org/abs/2509.13201`).

## Formatting

Use Prettier to keep Markdown and code tidy. To format only the file you changed:

```bash
npx prettier README.md --write
```

Replace `README.md` with the path to the file you modified. To format all currently staged files:

```bash
git diff --name-only --cached | xargs npx prettier --write
```
