# Insurance Capitol

Static agency website for Insurance Capitol (Mesa Motors LLC d/b/a Insurance Capitol), El Paso, Texas.
Navy, white and red brand system; personal, commercial and trucking coverage pages; dealership page;
customer service; a quick quote form (Netlify Forms) and five full insurance applications that post to the
RunTorque intake endpoint.

## Source

- `build.py`: page generator, navigation, copy and the quote and contact forms.
- `applications.py`: the five insurance applications, declared as data and rendered to forms that post to
  `https://runtorque.ai/api/applications`.
- `src/styles.css`: one stylesheet, each selector defined once; media blocks at the end.
- `src/site.js`: menu, repeatable application rows, validation and multipart submission.
- `src/logo.png`, `src/logo-mark.png`, `src/el-paso.webp`: brand artwork.
- `netlify.toml`: build command, redirects from the old site and security headers.
- `site/`: generated output. Netlify builds it with `python3 build.py`; it is not edited by hand.

## Pages

    /                         home with quick quote
    /auto  /home-insurance  /commercial  /trucking
    /dealers  /customer-service  /contact  /privacy
    /apply                    choose an application
    /apply/auto  /apply/home  /apply/commercial-auto  /apply/trucking  /apply/general-liability

## Forms

- `quote` and `contact` are Netlify Forms; delivery is configured in the Netlify dashboard (DEPLOY.md).
- The five applications (`application-auto`, `application-home`, `application-commercial-auto`,
  `application-trucking`, `application-general-liability`) post multipart to the RunTorque intake endpoint,
  which stores the application, encrypts Social Security numbers, keeps documents in private storage and
  emails the office. With scripts off the form posts natively and the endpoint redirects to the thank-you page.
- Every form has a honeypot field named `company`.
- Repeatable sections (drivers, vehicles, power units, trailers) render every row in the HTML. Rows after
  the first are hidden until added; with scripts off, all rows show.
- Documents: JPG, PNG, WEBP, HEIC or PDF, 4 MB each, 5 MB per application.

## Editing

Copy and page structure: `build.py`. Application questions: `applications.py` (add a field to a list and it
appears in the form and the email). Styles: `src/styles.css`.

    python3 build.py
    python3 -m http.server --directory site 8000

The local preview serves pages with their `.html` suffix (`/apply/auto.html`); Netlify serves them without.
Form submission is disabled on localhost by design.
