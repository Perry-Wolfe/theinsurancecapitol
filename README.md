# Insurance Capitol

A responsive, ten-page agency website with the existing Insurance Capitol capitol-and-shield logo, navy/red branding, personal and commercial coverage pages, dealership information, customer service and Netlify quote/contact forms.

## Source

- `build.py`: shared page generator, navigation, copy and form templates.
- `src/styles.css`: one shared design system and responsive layouts.
- `src/site.js`: accessible menu controls, validation and submission/error states.
- `src/logo.png`, `src/logo-mark.png`: extracted existing brand artwork.
- `src/el-paso.webp`: cropped skyline from existing marketing artwork.
- `site/`: compiled, ready-to-upload output.
- `netlify.toml`: build, redirects and security policy.
- `DEPLOY.md`: deployment and production verification.
- `IMPROVEMENTS.md`: fixes, limitations and integration priorities.

Build with Python 3: `python3 build.py`. No third-party Python packages required.
Follow DEPLOY.md to deploy and configure actual form delivery.
