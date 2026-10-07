# Deploy Insurance Capitol

This package preserves the existing Python + Netlify setup. No npm dependencies are required.

## Deploy from a repository

1. Upload `build.py`, `src/`, `netlify.toml`, README and the documentation to the existing website repository.
2. In Netlify, set build command to `python3 build.py` and publish directory to `site`.
3. Enable Netlify Forms detection and redeploy. Confirm both `quote` and `contact` are detected.
4. Configure a notification destination for each form. A notification inbox is not automatically configured by the source code.
5. Submit a test of each form on the deployed Netlify URL. Confirm the submission appears in the dashboard AND reaches the notification inbox. Test unsuccessful submission handling too.
6. Verify the domain and HTTPS in the existing Netlify account before changing DNS. Keep all email, verification and unrelated records. Use the DNS values Netlify currently provides for this specific project, rather than old hard-coded instructions.

## Deploy compiled files manually

The included `site/` directory is already built. Upload that directory to Netlify. For manual deployments, configure redirects and security headers in the account; the repository `netlify.toml` is intended for repository builds.

## Before going live

- Confirm current agency phone, hours, carrier appointments and licensing information. Business details were retained from the supplied source. The older marketing artwork uses a different phone number; only the logo and skyline were reused.
- Verify forms, email notifications, old URL redirects, the 404 page and mobile navigation on the actual deployment.
- No form request binds, changes or cancels coverage.
- This update has not changed DNS or published to the production account.

## Local preview

Run `python3 build.py`, then `python3 -m http.server --directory site 8000`.
Open `http://localhost:8000`. For the built-in Python preview server, inner pages can be opened with their `.html` suffix. Netlify serves the extensionless links in production.
The script explicitly prevents sending forms from localhost/file previews; no preview submission is represented as delivered.
