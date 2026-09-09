# Ziyue Luo · Academic Homepage

The public homepage is https://ziyueluocs.github.io/. It uses the selected classic design: a quiet reading column, blue links, contact information first, and publications grouped by year.

## Build and preview

Python 3.9 or newer is sufficient. There are no third-party build dependencies.

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
python3 -m http.server 4174 --bind 127.0.0.1 --directory _site
```

Open http://127.0.0.1:4174/. The build recreates `_site/`, which is generated output and is not committed.

## Content and appearance

- `_data/profile.json`: current position, affiliations, obfuscated contact email, office, biography, research description, and profile links. Biography and research fields contain small HTML paragraphs.
- `_pages/publications.md`: the publication list. Preserve the existing entry format; the builder groups entries by publication year and keeps complete author lists.
- `assets/pdf/CV.pdf`: the verified English CV downloaded from the homepage. Update its canonical Overleaf source first, compile and review the PDF, then copy it here.
- `assets/img/portrait.jpg`: the original portrait.
- `_templates/home.html`: the production page structure.
- `assets/css/academic.css` and `assets/js/academic.js`: the selected design and optional theme preference.

Asset URLs include content hashes, so updated styles and CVs do not reuse an older browser cache entry. The page remains readable and navigable with JavaScript disabled.

## Publication

GitHub Pages uses `.github/workflows/deploy.yml`. A push to `main` builds and validates the site, uploads only `_site/`, and deploys through the `github-pages` environment. Pull requests run the build and checks without publishing. The repository's Pages build type is GitHub Actions, and the environment permits `main`.

The public artifact contains the homepage, its required assets, a 404 page, a sitemap, and compatibility redirects:

- `/publications/` goes to `/#publications`.
- `/cv/` goes to the current `assets/pdf/CV.pdf`.

The `design-preview/` directory preserves the ten local design studies. It is not included in the public artifact. The older Jekyll/al-folio files are retained for reference; the new deployment does not run Jekyll or publish those sources.
