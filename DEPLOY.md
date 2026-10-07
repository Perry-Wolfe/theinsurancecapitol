# Deploying and configuring delivery

The site is already connected: GitHub repository, Netlify build (`python3 build.py`, publish `site`),
domain `www.theinsurancecapitol.com` on Netlify DNS records at GoDaddy. Pushing to the repository deploys.

## Delivery to the office

Applications: handled by RunTorque. The intake endpoint emails regina@carcapitol.com and
perry@carcapitol.com (set by `APPLICATION_RECIPIENTS` on the RunTorque Netlify project) and lists every
application at https://runtorque.ai/admin/applications. Nothing to configure on this project.

Quote and contact forms: Netlify Forms on this project. Once per form, two recipients each:

1. Netlify, this project, **Forms**: `quote` and `contact` are listed after the first deploy.
2. **Project configuration, Notifications, Form submission notifications, Add notification, Email notification.**
3. Event: New form submission. Form: pick one. Email: `regina@carcapitol.com`. Save.
4. Repeat for the same form with `perry@carcapitol.com`, then both again for the other form.

## Verify after deploy

1. Deploy the RunTorque update first (migration 008 and the APPLICATIONS_ENCRYPTION_KEY variable), then this site.
2. Open https://www.theinsurancecapitol.com/apply/auto, add a second driver, remove it, add it again.
3. Submit one test application with a small photo. Confirm the thank-you page, the email in both inboxes,
   and the application with its document at https://runtorque.ai/admin/applications.
4. Submit the quick quote on the home page; confirm it under Forms in this Netlify project.
5. Check `/trucking` and `/apply/trucking` on a phone.

## Housekeeping

- Quote and contact submissions sit in Netlify Forms (100 a month on the free plan). Applications live in
  the RunTorque database and are managed there.
- Local preview: `python3 build.py` then `python3 -m http.server --directory site 8000`. Form submission
  is disabled on localhost by design.
