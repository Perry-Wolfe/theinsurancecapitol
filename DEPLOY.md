# Deploying and configuring delivery

The site is already connected: GitHub repository, Netlify build (`python3 build.py`, publish `site`),
domain `www.theinsurancecapitol.com` on Netlify DNS records at GoDaddy. Pushing to the repository deploys.

## Delivery to the office

Applications: handled by RunTorque. The intake endpoint emails regina@carcapitol.com and
perry@carcapitol.com (set by `APPLICATION_RECIPIENTS` on the RunTorque Netlify project) and lists every
application at https://runtorque.ai/admin/applications. Nothing to configure on this project.

Quote and contact forms: also handled by RunTorque (types `quote` and `contact`, migration 023). Nothing to
configure on this project.

## Verify after deploy

1. Deploy the RunTorque update first (migration 008 and the APPLICATIONS_ENCRYPTION_KEY variable), then this site.
2. Open https://www.theinsurancecapitol.com/apply/auto, add a second driver, remove it, add it again.
3. Submit one test application with a small photo. Confirm the thank-you page, the email in both inboxes,
   and the application with its document at https://runtorque.ai/admin/applications.
4. Submit the quick quote on the home page; confirm the email and the entry at https://runtorque.ai/admin/applications.
5. Check `/trucking` and `/apply/trucking` on a phone.

## Housekeeping

- Quote requests, messages and applications all live in the RunTorque database and are managed there.
- Local preview: `python3 build.py` then `python3 -m http.server --directory site 8000`. Form submission
  is disabled on localhost by design.
