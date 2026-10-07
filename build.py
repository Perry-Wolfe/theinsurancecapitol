"""Generates the static pages for theinsurancecapitol.com.

Run: python3 build.py
Output: ./site (what gets deployed)
"""
import os, shutil
from html import escape
from applications import APPLICATIONS, render_application, render_index

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'src')
OUT = os.path.join(ROOT, 'site')

SITE = 'https://www.theinsurancecapitol.com'
PHONE = '915-760-4411'
PHONE_HREF = 'tel:+19157604411'
FAX = '915-581-3900'
ADDRESS = '6354 N Mesa St, El Paso, TX 79912'
MAPS = 'https://maps.app.goo.gl/CQRWaQi2WgZJBfut5'
RUNTORQUE = 'https://runtorque.ai'

NAV = [
    ('index.html', '/', 'Home'),
    ('auto.html', '/auto', 'Auto'),
    ('home-insurance.html', '/home-insurance', 'Home &amp; renters'),
    ('commercial.html', '/commercial', 'Commercial'),
    ('trucking.html', '/trucking', 'Trucking'),
    ('dealers.html', '/dealers', 'Dealers'),
    ('customer-service.html', '/customer-service', 'Customer service'),
    ('contact.html', '/contact', 'Contact'),
]

LOGO = '<img src="/logo.png" alt="Insurance Capitol" width="244" height="245">'


def header(active):
    links = []
    for file, path, label in NAV[1:]:
        current = ' aria-current="page"' if file == active else ''
        links.append(f'<a href="{path}"{current}>{label}</a>')
    links.append(f'<a class="call" href="{PHONE_HREF}">Call {PHONE}</a>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="utility"><div class="wrap"><span>Independent insurance. Personal attention.</span><span>Texas · New Mexico · California <span class="utility-language">/ Hablamos español</span></span></div></div>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/">{LOGO.replace("/logo.png", "/logo-mark.png")}<div><b>Insurance<span>Capitol</span></b></div></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">{''.join(links)}</nav>
  </div>
</header>'''


FOOTER = f'''<footer class="foot">
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="footer-logo" href="/">{LOGO}</a>
        <address class="addr">{ADDRESS}<br><a href="{PHONE_HREF}">{PHONE}</a><br>Fax {FAX}</address>
        <p class="foot-note">Hablamos español.</p>
      </div>
      <div>
        <h3>Insurance</h3>
        <ul><li><a href="/auto">Auto</a></li><li><a href="/home-insurance">Home and renters</a></li><li><a href="/commercial">Commercial</a></li><li><a href="/trucking">Commercial trucking</a></li><li><a href="/apply">Start an application</a></li></ul>
      </div>
      <div>
        <h3>Help</h3>
        <ul><li><a href="/customer-service">Customer service</a></li><li><a href="/contact">Contact</a></li><li><a href="/privacy">Privacy</a></li></ul>
      </div>
      <div>
        <h3>Partners</h3>
        <ul><li><a href="/dealers">For dealerships</a></li><li><a href="{RUNTORQUE}" rel="noopener">RunTorque</a></li></ul>
      </div>
    </div>
    <div class="legal">
      <p>Insurance Capitol is a d/b/a of Mesa Motors LLC, a Texas general lines agency, property and casualty, license 3216657 (NPN 21285254). Perry T. Wolfe, licensed producer: Texas 3186385, New Mexico 21216112, California 4442693. In California the agency does business as Insurance Capitol Services.</p>
      <p>Coverage is underwritten by the carrier named on your policy and is subject to that carrier's eligibility, underwriting and terms. Quotes are estimates until a carrier issues the policy. Insurance Capitol is the agency of record on policies quoted or bound through the RunTorque platform; RunTorque (Torque.ai Incorporated) is a software platform and does not sell insurance.</p>
      <p>&copy; <span data-year>2026</span> Mesa Motors LLC d/b/a Insurance Capitol. All rights reserved.</p>
    </div>
  </div>
</footer>
<script src="/site.js" defer></script>'''


def page(file, title, description, body, active=None, path=None):
    canonical = SITE + (path if path is not None else '/' + file[:-len('.html')])
    if file == 'index.html':
        canonical = SITE + '/'
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="/logo-mark.png" type="image/png">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
<meta name="theme-color" content="#071b3e">
{'<meta name="robots" content="noindex">' if file in ('404.html', 'thank-you.html') else ''}
</head>
<body>
{header(active or file)}
<main id="main">
{body}
</main>
{FOOTER}
</body>
</html>
'''
    target = os.path.join(OUT, file)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, 'w') as f:
        f.write(html)


QUOTE_FORM = f'''<aside class="quote-card" id="quote" aria-labelledby="quote-title">
  <header>
    <h2 id="quote-title">Request a quote</h2>
    <p>Tell us what you need. Our team will help you compare available coverage.</p>
  </header>
  <form name="quote" method="POST" action="/thank-you" data-netlify="true" netlify-honeypot="company">
    <input type="hidden" name="form-name" value="quote">
    <p class="hidden" aria-hidden="true"><label>Company <input name="company" tabindex="-1" autocomplete="off"></label></p>
    <fieldset class="choices">
      <legend>What do you need covered? <span class="hint">Select all that apply</span></legend>
      <div class="chips">
        <label><input type="checkbox" name="coverage" value="Auto"> Auto</label>
        <label><input type="checkbox" name="coverage" value="SR-22"> SR-22</label>
        <label><input type="checkbox" name="coverage" value="Home or renters"> Home or renters</label>
        <label><input type="checkbox" name="coverage" value="Commercial"> Commercial</label>
      </div>
    </fieldset>
    <div class="row-2">
      <div class="field"><label for="q-name">Full name</label><input id="q-name" name="name" autocomplete="name" required></div>
      <div class="field"><label for="q-phone">Mobile phone</label><input id="q-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" required></div>
    </div>
    <div class="row-2">
      <div class="field"><label for="q-zip">ZIP code</label><input id="q-zip" name="zip" inputmode="numeric" autocomplete="postal-code" pattern="[0-9]{{5}}" title="Five digit ZIP code" required></div>
      <div class="field"><label for="q-lang">Preferred language</label><select id="q-lang" name="language"><option>English</option><option>Español</option></select></div>
    </div>
    <div class="row-2">
      <div class="field"><label for="q-email">Email <span class="hint">(optional)</span></label><input id="q-email" name="email" type="email" autocomplete="email"></div>
      <div class="field"><label for="q-method">Contact preference</label><select id="q-method" name="contact-preference"><option>Phone call</option><option>Text message</option><option>Email</option></select></div>
    </div>
    <div class="field">
      <label for="q-notes">Anything we should know? <span class="hint">(vehicle, current carrier, dealership, lienholder)</span></label>
      <textarea id="q-notes" name="notes" rows="3"></textarea>
    </div>
    <p class="form-status" role="status" aria-live="polite"></p>
    <button class="btn btn-accent btn-block" type="submit">Send quote request</button>
    <p class="consent">By sending this request you agree that Insurance Capitol may call or text you at the number provided about your quote. Message and data rates may apply. Reply STOP to opt out of texts. We do not sell your information. <a href="/privacy">Privacy policy</a>.</p>
    <p class="consent">Ready to give us everything at once? <a href="/apply">Start a full application</a>.</p>
  </form>
</aside>'''


def license_band():
    return '''<section class="license" aria-labelledby="lic-title">
  <div class="wrap">
    <div>
      <h2 id="lic-title">Licensed in Texas, New Mexico and California</h2>
      <p>Licensing information for our customers and business partners.</p>
    </div>
    <dl>
      <div><dt>Texas general lines agency, P&amp;C</dt><dd>3216657<small>Mesa Motors LLC d/b/a Insurance Capitol, NPN 21285254</small></dd></div>
      <div><dt>Texas producer, P&amp;C</dt><dd>3186385<small>Perry T. Wolfe, NPN 21216112</small></dd></div>
      <div><dt>New Mexico and California producer</dt><dd>21216112 / 4442693<small>Casualty and property</small></dd></div>
    </dl>
  </div>
</section>'''


CTA = f'''<section class="cta">
  <div class="wrap">
    <h2>Ready when you are.</h2>
    <div class="actions">
      <a class="btn btn-primary" href="/#quote">Request a quote</a>
      <a class="btn btn-outline" href="{PHONE_HREF}">Call {PHONE}</a>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- pages

INDEX = f'''<section class="hero"><div class="wrap">
  <div class="hero-copy">
    <p class="eyebrow">INSURANCE, WITH YOUR LIFE IN MIND</p>
    <h1>Great coverage.<br>Better <span>possibilities.</span></h1>
    <p class="lead">Your car. Your home. Your business. Get coverage that fits, with an independent agency that puts you first.</p>
    <div class="hero-actions"><a class="btn btn-accent" href="#quote">Find my coverage</a><a class="text-link" href="{PHONE_HREF}">Talk to our team</a></div>
    <div class="hero-proof"><div><strong>More choice</strong><span>Multiple insurance markets</span></div><div><strong>Real people</strong><span>English &amp; español</span></div></div>
    <div class="local-image"><img src="/el-paso.webp" alt="El Paso skyline and mountains at sunset" width="469" height="157"><div><span>ROOTED IN EL PASO</span><strong>Here for what’s next.</strong></div></div>
  </div>{QUOTE_FORM}
</div></section>
<section class="carrier-strip"><div class="wrap"><p class="eyebrow">CHOICE THROUGH OUR INSURANCE MARKETS</p><ul class="carriers"><li>Progressive</li><li>Travelers</li><li>The General</li><li>Paramount</li><li>BHHC</li><li>TAPCO</li></ul><p class="small">Availability varies by state, coverage and underwriting requirements.</p></div></section>
<section class="section"><div class="wrap"><div class="section-head"><p class="eyebrow">COVERAGE FOR EVERY CHAPTER</p><h2>Protect what moves you.</h2><p>Explore your options. We’ll help you make sense of the details.</p></div>
<div class="grid-3 grid-4">
<a class="coverage-card" href="/auto"><span class="card-number">01 / ON THE ROAD</span><h3>Auto insurance</h3><p>Everyday driving, financed vehicles and SR-22 filings. Find options for your situation.</p><span class="card-link">Explore auto coverage</span></a>
<a class="coverage-card" href="/home-insurance"><span class="card-number">02 / AT HOME</span><h3>Home &amp; renters</h3><p>From your first apartment to your next home. Protect your space and what’s inside.</p><span class="card-link">Explore home coverage</span></a>
<a class="coverage-card" href="/commercial"><span class="card-number">03 / IN BUSINESS</span><h3>Commercial</h3><p>Vehicles, operations and dealership inventory. Coverage built around how you work.</p><span class="card-link">Explore business coverage</span></a>
<a class="coverage-card" href="/trucking"><span class="card-number">04 / ON THE HIGHWAY</span><h3>Commercial trucking</h3><p>Liability, cargo, physical damage and federal filings for motor carriers and owner-operators.</p><span class="card-link">Explore trucking coverage</span></a>
</div></div></section>
<section class="section dealer-feature"><div class="wrap grid-2"><div><p class="eyebrow">FOR DEALERSHIPS</p><h2>A smoother road<br>from approval to delivery.</h2><p class="lead">Connect the insurance step to your deal through RunTorque, with Insurance Capitol providing licensed insurance support.</p><a class="btn btn-accent" href="/dealers">Discover dealership support</a></div><ol class="steps"><li><h3>Share the details</h3><p>With customer consent, send the vehicle and driver information.</p></li><li><h3>Compare coverage</h3><p>Our team reviews available markets and prepares options.</p></li><li><h3>Get proof of insurance</h3><p>Once coverage is bound, documentation goes to the customer, dealer and lender.</p></li></ol></div></section>
{license_band()}
<section class="section"><div class="wrap faq"><div><p class="eyebrow">A LITTLE CLARITY</p><h2>Good questions.<br>Clear answers.</h2><p>Need something more specific? <a href="/contact">Talk to our team.</a></p></div><div>
<details><summary>Can you help if I have no prior insurance?</summary><p>We can explore carriers that consider drivers without prior coverage. Eligibility and pricing depend on your details and the carrier.</p></details>
<details><summary>Can you send proof to my dealer or lender?</summary><p>Yes. Once your policy is bound, we can provide proof of insurance and help confirm the lienholder information.</p></details>
<details><summary>Does requesting a quote start my coverage?</summary><p>No. A request does not bind, change or cancel coverage. Coverage begins only after the carrier confirms issuance and the effective date.</p></details>
<details><summary>¿Puedo recibir ayuda en español?</summary><p>Sí. Selecciona Español en el formulario o llama a nuestro equipo. Te ayudamos a entender tus opciones de cobertura.</p></details>
</div></div></section>{CTA}'''

AUTO = f'''<section class="page-head"><div class="wrap"><h1>Auto insurance</h1><p>Texas, New Mexico and California. Explore coverage and payment options for your driving situation.</p></div></section>
<section class="section">
  <div class="wrap grid-2">
    <div class="prose">
      <h2>Who we help</h2>
      <p>Most of our customers are buying or financing a vehicle and need coverage today. Many have been quoted high rates elsewhere or told no. We place policies for:</p>
      <ul>
        <li>Drivers with no prior insurance or a lapse in coverage</li>
        <li>SR-22 filings after a suspension, DWI or uninsured accident</li>
        <li>Drivers with a foreign license, matrícula consular or passport as identification</li>
        <li>Financed vehicles that require full coverage and a lienholder listed</li>
        <li>Young drivers, new residents, and drivers with tickets or accidents</li>
      </ul>
      <h2>What to have ready</h2>
      <ul>
        <li>Driver's license or other government ID for every driver in the household</li>
        <li>Vehicle identification number (VIN) or the year, make and model</li>
        <li>Garaging address</li>
        <li>Lienholder name if the vehicle is financed</li>
        <li>Current or prior insurance information, if any</li>
      </ul>
      <h2>Payments</h2>
      <p>Low down payment options are available from several carriers, with monthly, quarterly or paid-in-full plans. Payments are made directly to the carrier, by card, bank draft or in our office.</p>
      <h2>Ready to apply</h2>
      <p>The <a href="/apply/auto">auto application</a> collects every driver and vehicle in one pass so we can quote carriers without calling you back for details.</p>
    </div>
    <div>
      {QUOTE_FORM}
    </div>
  </div>
</section>
{license_band()}
{CTA}'''

HOME = f'''<section class="page-head"><div class="wrap"><h1>Home, renters and condo</h1><p>Protect the place you live and satisfy your mortgage lender, with one agent who also handles your auto.</p></div></section>
<section class="section">
  <div class="wrap grid-2">
    <div class="prose">
      <h2>Homeowners</h2>
      <p>Dwelling, other structures, personal property, loss of use and liability. We quote replacement cost coverage and review deductibles for wind and hail, which matter in West Texas.</p>
      <h2>Renters</h2>
      <p>Covers your belongings and your liability for a few dollars a month. Many landlords and apartment communities require it, and bundling with auto usually offsets the cost.</p>
      <h2>Condo</h2>
      <p>Coverage for the interior of your unit and your belongings, matched to what your association's master policy already covers.</p>
      <h2>Lender and closing requirements</h2>
      <p>If you are closing on a home, send us the lender's insurance requirements and the closing date. We deliver the evidence of insurance to your lender or title company before closing.</p>
      <h2>Ready to apply</h2>
      <p>The <a href="/apply/home">home application</a> asks for the property details carriers rate on, so the first quote we send is the real one.</p>
    </div>
    <div>{QUOTE_FORM}</div>
  </div>
</section>
{CTA}'''

COMMERCIAL = f'''<section class="page-head"><div class="wrap"><h1>Commercial insurance</h1><p>Commercial auto, general liability and garage coverage for small businesses, contractors and dealerships in Texas and New Mexico.</p></div></section>
<section class="section">
  <div class="wrap grid-2">
    <div class="prose">
      <h2>Commercial auto</h2>
      <p>Owned, hired and non-owned vehicles for contractors, delivery, landscaping, cleaning and other service businesses. Higher liability limits for contracts that require them.</p>
      <h2>General liability</h2>
      <p>Premises and operations coverage, with certificates of insurance issued to your customers or landlord on request.</p>
      <h2>Garage and dealer coverage</h2>
      <p>Garage liability, dealer open lot (physical damage on inventory), and dealer plates coverage for licensed dealers. We operate a dealership ourselves, so we know what the Texas DMV and your floorplan lender require.</p>
      <h2>Trucking</h2>
      <p>Tractors, semi trailers and for-hire operations are written on trucking programs with their own filings and limits. See <a href="/trucking">commercial trucking</a>.</p>
      <h2>How to get a commercial quote</h2>
      <p>Use the form with "Commercial" selected for a quick callback, or go straight to the <a href="/apply/commercial-auto">commercial auto application</a> or <a href="/apply/general-liability">general liability application</a> and we will rate it the same business day.</p>
    </div>
    <div>{QUOTE_FORM}</div>
  </div>
</section>
{CTA}'''

TRUCKING = f'''<section class="page-head"><div class="wrap"><h1>Commercial trucking insurance</h1><p>Liability, cargo, physical damage and the filings that keep your authority active. For motor carriers, owner-operators and new ventures based in Texas and New Mexico.</p></div></section>
<section class="section">
  <div class="wrap grid-2">
    <div class="prose">
      <h2>Coverages we place</h2>
      <ul>
        <li><strong>Auto liability</strong> at $750,000 or $1,000,000, with the MCS-90 endorsement and BMC-91X filing for interstate authority and Form E for intrastate.</li>
        <li><strong>Motor truck cargo</strong> for the freight you haul, including reefer breakdown and debris removal where needed.</li>
        <li><strong>Physical damage</strong> on tractors and trailers, with the lienholder listed.</li>
        <li><strong>General liability</strong> for loading, unloading and premises exposure that shippers and brokers ask for.</li>
        <li><strong>Non-trucking liability and bobtail</strong> for owner-operators leased to a carrier.</li>
        <li><strong>Trailer interchange</strong> and <strong>occupational accident</strong> when your contracts require them.</li>
      </ul>
      <h2>Who we write</h2>
      <ul>
        <li>New ventures with authority pending or under one year</li>
        <li>Owner-operators with one to five units, leased on or running their own authority</li>
        <li>Small fleets in general freight, flatbed, reefer, auto hauling, dump and hot shot</li>
        <li>Border and cross-dock operations in El Paso and Santa Teresa</li>
      </ul>
      <h2>What carriers will ask for</h2>
      <p>USDOT and MC numbers, the equipment list with VINs and values, every driver's CDL and date of birth, three years of loss runs if you have been insured, and your radius and commodities. The <a href="/apply/trucking">trucking application</a> collects all of it in one pass.</p>
      <p>Carriers run MVRs on every listed driver and check your FMCSA safety record. Tell us about violations up front; it changes which market we approach, not whether we can help.</p>
    </div>
    <div>
      <div class="quote-card">
        <header><h2>Start your trucking application</h2><p>About 15 minutes. Have your USDOT number, VINs and driver CDLs ready.</p></header>
        <div class="app-cta">
          <a class="btn btn-accent btn-block" href="/apply/trucking">Open the application</a>
          <p class="small">Or call <a href="{PHONE_HREF}">{PHONE}</a> and we will take it over the phone.</p>
        </div>
      </div>
      <div class="notice mt-md">
        <strong>Filings.</strong> Federal filings (BMC-91X, MCS-90) are made by the carrier after the policy is bound, usually within one business day. Plan for that when you schedule your authority activation or a shipper onboarding date.
      </div>
    </div>
  </div>
</section>
{license_band()}
{CTA}'''

DEALERS = f'''<section class="page-head"><div class="wrap"><h1>For dealerships</h1><p>Deliver cars with coverage already bound. Insurance Capitol is the licensed agency on the insurance step of the RunTorque platform.</p></div></section>
<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>What changes at your F&amp;I desk</h2>
      <p>Every financed customer needs proof of coverage before delivery. Today that means the customer leaves to call around, or your F&amp;I manager spends an hour on the phone. With RunTorque the coverage step is part of the deal.</p>
    </div>
    <ol class="steps">
      <li><h3>Submit the deal on RunTorque</h3><p>Identity, income and vehicle are verified once. Lenders see a complete package.</p></li>
      <li><h3>Customer consents, we quote</h3><p>Approved deal fields move to Insurance Capitol. We review available carriers and coordinate binding after customer acceptance and carrier approval.</p></li>
      <li><h3>Proof returns to you and the lender</h3><p>ID card and binder are attached to the deal with the lienholder listed. Funding packages go out clean.</p></li>
    </ol>
  </div>
</section>
<section class="section alt">
  <div class="wrap grid-2">
    <div class="prose">
      <h2>Why dealers use it</h2>
      <ul>
        <li>Coordinate coverage before delivery, subject to carrier approval and payment.</li>
        <li>Fewer funding delays. Lenders receive proof with the lienholder already correct.</li>
        <li>Nonstandard customers get placed. We carry markets for SR-22, foreign ID and no prior coverage.</li>
        <li>Your customer stays in your showroom instead of walking out to shop insurance.</li>
      </ul>
      <h2>How to get started</h2>
      <p>Dealerships join the RunTorque network at <a href="{RUNTORQUE}" rel="noopener">runtorque.ai</a>. Insurance is included in the workflow for every participating store. If you are not on RunTorque yet and want insurance help for your deliveries in El Paso today, call us directly.</p>
      <p><a class="btn btn-primary" href="{RUNTORQUE}" rel="noopener">Visit RunTorque</a> <a class="btn btn-outline" href="{PHONE_HREF}">Call {PHONE}</a></p>
    </div>
    <div class="notice">
      <strong>For carriers and lenders.</strong> Insurance Capitol (Mesa Motors LLC) holds Texas general lines agency license 3216657, NPN 21285254. The platform is RunTorque, operated by Torque.ai Incorporated; the agency of record on every policy is Insurance Capitol. Appointment and integration inquiries: <a href="{PHONE_HREF}">{PHONE}</a> or the <a href="/contact">contact form</a>.
    </div>
  </div>
</section>
{license_band()}
{CTA}'''

SERVICE = f'''<section class="page-head"><div class="wrap"><h1>Customer service</h1><p>ID cards, payments, policy changes and claims. Our team can help you find the right next step.</p></div></section>
<section class="section">
  <div class="wrap contact-grid">
    <ul class="service-list">
      <li><h3>Proof of insurance or ID card</h3><p>Call or text {PHONE} with your name and vehicle. We send a copy to you, your dealer or your lender.</p></li>
      <li><h3>Make a payment</h3><p>Payments go directly to your carrier. Use the carrier's number below, or call us and we will take the payment with you on the line.</p></li>
      <li><h3>Add or remove a vehicle or driver</h3><p>Send the VIN or driver's license and the effective date you need. Most changes are issued the same day.</p></li>
      <li><h3>Lienholder or address change</h3><p>Tell us the new lender or address and we update the policy and resend proof to whoever needs it.</p></li>
      <li><h3>File a claim</h3><p>Report claims directly to your carrier using the numbers below so it is logged immediately. Then call us and we will stay on it with you.</p></li>
    </ul>
    <div>
      <h2>Carrier service and claims</h2>
      <div class="table-scroll" tabindex="0" role="region" aria-label="Carrier service and claims numbers"><table class="plain">
        <thead><tr><th>Carrier</th><th>Customer service</th><th>Claims</th></tr></thead>
        <tbody>
          <tr><td>Progressive</td><td><a href="tel:+18007764737">800-776-4737</a></td><td><a href="tel:+18002744499">800-274-4499</a></td></tr>
          <tr><td>The General</td><td><a href="tel:+18443280306">844-328-0306</a></td><td><a href="tel:+18002801466">800-280-1466</a></td></tr>
          <tr><td>Travelers</td><td><a href="tel:+18885645043">888-564-5043</a></td><td><a href="tel:+18002524633">800-252-4633</a></td></tr>
        </tbody>
      </table></div>
      <p class="small mt-sm">Numbers are the carriers' published lines and may change. Your policy documents are the final word.</p>
      <div class="notice-green mt-md"><strong>Not sure who your carrier is?</strong> Call us at <a href="{PHONE_HREF}">{PHONE}</a>. We look it up by your name or VIN.</div>
    </div>
  </div>
</section>
{CTA}'''

CONTACT = f'''<section class="page-head"><div class="wrap"><h1>Contact</h1><p>Walk in, call, text or send a note. Hablamos español.</p></div></section>
<section class="section">
  <div class="wrap contact-grid">
    <div>
      <h2>Office</h2>
      <address class="addr">
        Insurance Capitol<br>{ADDRESS}<br>
        <a href="{MAPS}" rel="noopener">Open in Google Maps</a>
      </address>
      <h2 class="mt">Phone</h2>
      <p><a href="{PHONE_HREF}">{PHONE}</a> (call or text)<br>Fax {FAX}</p>
      <h2 class="mt">Hours</h2>
      <dl class="hours">
        <dt>Monday to Friday</dt><dd>9:00 am to 6:00 pm</dd>
        <dt>Saturday</dt><dd>10:00 am to 3:00 pm</dd>
        <dt>Sunday</dt><dd>Closed</dd>
      </dl>
      <p class="small mt-sm">Dealership deliveries outside these hours: call the office line and leave a message with the dealer name; we monitor it.</p>
    </div>
    <div class="quote-card">
      <header><h2>Send a message</h2><p>For quotes, use the quote form. For anything else, this reaches the office directly.</p></header>
      <form name="contact" method="POST" action="/thank-you" data-netlify="true" netlify-honeypot="company">
        <input type="hidden" name="form-name" value="contact">
        <p class="hidden" aria-hidden="true"><label>Company <input name="company" tabindex="-1" autocomplete="off"></label></p>
        <div class="row-2">
          <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" autocomplete="name" required></div>
          <div class="field"><label for="c-phone">Phone or email</label><input id="c-phone" name="contact" required></div>
        </div>
        <div class="field"><label for="c-topic">Topic</label>
          <select id="c-topic" name="topic">
            <option>Existing policy</option><option>Dealership partnership</option><option>Carrier appointment or integration</option><option>Other</option>
          </select>
        </div>
        <div class="field"><label for="c-msg">Message</label><textarea id="c-msg" name="message" rows="5" required></textarea></div>
        <p class="form-status" role="status" aria-live="polite"></p><button class="btn btn-primary btn-block" type="submit">Send message</button>
      </form>
    </div>
  </div>
</section>'''

THANKS = f'''<section class="section">
  <div class="wrap prose">
    <h1>Got it. We will be in touch.</h1>
    <p class="lead">Our team will review your request and follow up during business hours. If you need coverage right now, call <a href="{PHONE_HREF}">{PHONE}</a> and tell us you are at a dealership.</p>
    <p><a class="btn btn-primary" href="/">Back to the home page</a></p>
  </div>
</section>'''

PRIVACY = f'''<section class="page-head"><div class="wrap"><h1>Privacy</h1><p>How Insurance Capitol handles the information you give us.</p></div></section>
<section class="section"><div class="wrap prose">
  <h2>What we collect</h2>
  <p>When you request a quote or contact us, we collect what you enter: name, phone, ZIP code, language preference, and anything you write in the message. To quote a policy we will also ask for driver's license or other identification, date of birth, vehicle information and address. If you are a RunTorque dealership customer, the dealership shares vehicle, driver and financing details with us only after you consent on the platform.</p>
  <h2>How we use it</h2>
  <p>To prepare quotes, bind and service policies, communicate with you about them, and meet legal and carrier requirements. Information is shared with the insurance carriers we quote and with your lender or dealership when proof of insurance is required. We do not sell your information.</p>
  <h2>Texting</h2>
  <p>If you give us a mobile number we may call or text you about your quote or policy. Reply STOP to any text to opt out.</p>
  <h2>Website</h2>
  <p>Form submissions are processed by our hosting provider, Netlify, and delivered to our office. This site does not use advertising trackers.</p>
  <h2>Applications</h2>
  <p>Insurance applications ask for the information carriers rate on: dates of birth, Social Security numbers where you have one, driver's license or CDL numbers, vehicle identification numbers, lienholders and loss history, and let you attach a copy of a license, registration or loss runs. Applications are sent over an encrypted connection to our secure system operated on the RunTorque platform, where Social Security numbers are stored encrypted and documents are kept in private storage. They are used only to quote and place coverage. Do not include payment card numbers; we collect payment information directly with the carrier when a policy is issued.</p>
  <h2>Questions</h2>
  <p>Call <a href="{PHONE_HREF}">{PHONE}</a> or write to Insurance Capitol, {ADDRESS}.</p>
</div></section>'''

NOT_FOUND = f'''<section class="section">
  <div class="wrap prose">
    <h1>That page is not here.</h1>
    <p class="lead">The address may be old. The pages below cover everything on the site, or call <a href="{PHONE_HREF}">{PHONE}</a>.</p>
    <p><a class="btn btn-primary" href="/">Home</a> <a class="btn btn-outline" href="/#quote">Request a quote</a> <a class="btn btn-outline" href="/customer-service">Customer service</a></p>
  </div>
</section>'''


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for name in os.listdir(SRC):
        shutil.copy2(os.path.join(SRC, name), os.path.join(OUT, name))

    page('index.html', 'Insurance Capitol | Auto, home and commercial insurance in El Paso, TX',
         'Independent insurance agency in El Paso writing auto, SR-22, home and commercial coverage in Texas, New Mexico and California. Coverage subject to carrier approval. Licensed agency on the RunTorque dealer platform.',
         INDEX.replace('value="Auto"', 'value="Auto" checked', 1))
    page('auto.html', 'Auto insurance in El Paso | Insurance Capitol',
         'Auto insurance for every driving record: no prior coverage, SR-22, foreign license, financed vehicles. Coverage options in Texas, New Mexico and California.',
         AUTO.replace('value="Auto"', 'value="Auto" checked', 1))
    page('home-insurance.html', 'Home, renters and condo insurance | Insurance Capitol',
         'Homeowners, renters and condo insurance in El Paso and across Texas, bundled with auto. Lender requirements handled before closing.',
         HOME.replace('value="Home or renters"', 'value="Home or renters" checked', 1))
    page('commercial.html', 'Commercial insurance | Insurance Capitol',
         'Commercial auto, general liability, garage liability and dealer open lot coverage for small businesses and dealerships in Texas and New Mexico.',
         COMMERCIAL.replace('value="Commercial"', 'value="Commercial" checked', 1))
    page('trucking.html', 'Commercial trucking insurance | Insurance Capitol',
         'Trucking insurance for motor carriers and owner-operators in Texas and New Mexico: auto liability with MCS-90 and BMC-91X filings, motor truck cargo, physical damage, non-trucking liability.',
         TRUCKING)
    page('apply/index.html', 'Start an application | Insurance Capitol',
         'Online insurance applications for personal auto, home, commercial auto, commercial trucking and general liability. Delivered to our El Paso office the moment you submit.',
         render_index(PHONE_HREF, PHONE), active='apply/index.html', path='/apply')
    for app in APPLICATIONS:
        page(app['file'], f"{app['title']} | Insurance Capitol", app['intro'],
             render_application(app, PHONE, PHONE_HREF), active='apply/index.html', path=app['path'])
    page('dealers.html', 'For dealerships | Insurance Capitol and RunTorque',
         'Insurance Capitol is the licensed agency on the insurance step of the RunTorque dealer-to-lender platform. Coverage bound before delivery, proof returned to dealer and lender.',
         DEALERS)
    page('customer-service.html', 'Customer service | Insurance Capitol',
         'ID cards, payments, policy changes and claims for Insurance Capitol customers. Carrier service and claims numbers.',
         SERVICE)
    page('contact.html', 'Contact Insurance Capitol | El Paso, TX',
         'Insurance Capitol, 6354 N Mesa St, El Paso, TX 79912. Call or text 915-760-4411. Hablamos español.',
         CONTACT)
    page('thank-you.html', 'Thank you | Insurance Capitol', 'Your request was received.', THANKS, active='index.html')
    page('privacy.html', 'Privacy | Insurance Capitol', 'How Insurance Capitol handles your information.', PRIVACY, active='index.html')
    page('404.html', 'Page not found | Insurance Capitol', 'Page not found.', NOT_FOUND, active='index.html', path='/404')

    pages = ['', 'auto', 'home-insurance', 'commercial', 'trucking', 'dealers', 'customer-service', 'contact', 'privacy', 'apply']
    pages += [app['path'].lstrip('/') for app in APPLICATIONS]
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for p in pages:
            f.write(f'  <url><loc>{SITE}/{p}</loc></url>\n')
        f.write('</urlset>\n')
    total = sum(len(files) for _, _, files in os.walk(OUT))
    print('built', total, 'files in', OUT)


if __name__ == '__main__':
    main()
