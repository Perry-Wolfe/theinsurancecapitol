"""Insurance application forms, one per line of business.

Each application is declared as data (sections of fields, some repeatable) and
rendered to a form that posts to the RunTorque intake endpoint, which stores the
application, encrypts Social Security numbers and emails the office. Repeatable
sections render every row in the HTML; rows after the first are hidden until the
visitor adds them (site.js), and all rows show when scripts are off.
"""

INTAKE_URL = 'https://runtorque.ai/api/applications'
from html import escape

STATES = ['TX', 'NM', 'CA', 'AZ', 'OK', 'LA', 'CO', 'Other']
YES_NO = ['No', 'Yes']


def text(name, label, required=False, hint=None, **attrs):
    return {'type': 'text', 'name': name, 'label': label, 'required': required, 'hint': hint, 'attrs': attrs}


def select(name, label, options, required=False, hint=None):
    return {'type': 'select', 'name': name, 'label': label, 'options': options, 'required': required, 'hint': hint}


def area(name, label, hint=None, required=False):
    return {'type': 'textarea', 'name': name, 'label': label, 'hint': hint, 'required': required}


def upload(name, label, hint=None):
    return {'type': 'file', 'name': name, 'label': label, 'hint': hint}


def ssn(name='ssn', label='Social Security number', required=False):
    return text(name, label, required, hint='Used to rate the policy. Leave blank if you do not have one. Sent and stored encrypted.',
                inputmode='numeric', autocomplete='off', pattern='[0-9]{3}-?[0-9]{2}-?[0-9]{4}',
                title='Nine digits, with or without dashes', spellcheck='false')


def section(title, fields, intro=None):
    return {'title': title, 'intro': intro, 'fields': fields, 'repeat': None}


def repeat(title, item, fields, count, intro=None):
    return {'title': title, 'intro': intro, 'fields': fields, 'repeat': {'item': item, 'count': count}}


CONTACT = section('Your contact information', [
    text('name', 'Full name', True, attrs=dict(autocomplete='name')),
    text('phone', 'Mobile phone', True, type='tel', autocomplete='tel', inputmode='tel'),
    text('email', 'Email', True, type='email', autocomplete='email'),
    select('language', 'Preferred language', ['English', 'Español']),
    text('address', 'Street address', True, autocomplete='street-address'),
    text('city', 'City', True, autocomplete='address-level2'),
    select('state', 'State', STATES, True),
    text('zip', 'ZIP code', True, inputmode='numeric', autocomplete='postal-code', pattern='[0-9]{5}', title='Five digit ZIP code'),
])

BUSINESS = section('Business information', [
    text('business-name', 'Legal business name', True, autocomplete='organization'),
    text('dba', 'DBA, if different'),
    select('entity-type', 'Entity type', ['Sole proprietor', 'LLC', 'Corporation', 'Partnership', 'Other']),
    text('years-in-business', 'Years in business', True, inputmode='numeric'),
    text('fein', 'Federal EIN', hint='Leave blank for a sole proprietor'),
    ssn('owner-ssn', 'Owner Social Security number'),
    text('contact-name', 'Contact name', True, autocomplete='name'),
    text('phone', 'Phone', True, type='tel', autocomplete='tel', inputmode='tel'),
    text('email', 'Email', True, type='email', autocomplete='email'),
    text('address', 'Business address', True, autocomplete='street-address'),
    text('city', 'City', True),
    select('state', 'State', STATES, True),
    text('zip', 'ZIP code', True, inputmode='numeric', pattern='[0-9]{5}', title='Five digit ZIP code'),
])

PRIOR_INSURANCE = section('Current or prior insurance', [
    select('prior-insurance', 'Do you have insurance now?', ['Yes', 'No, lapsed less than 30 days', 'No, lapsed more than 30 days', 'Never insured'], True),
    text('prior-carrier', 'Current or most recent carrier'),
    text('prior-expiration', 'Policy expiration date', type='date'),
    text('desired-start', 'When do you need coverage to start?', True, type='date'),
])

DRIVER_FIELDS = [
    text('name', 'Full legal name', True),
    text('dob', 'Date of birth', True, type='date'),
    ssn(),
    select('license-type', 'License type', ['US driver\'s license', 'Foreign license', 'Matrícula consular', 'Passport', 'Permit', 'No license'], True),
    text('license-number', 'License or ID number'),
    select('license-state', 'License state or country', STATES + ['Mexico'], True),
    select('marital', 'Marital status', ['Single', 'Married', 'Divorced', 'Widowed']),
    select('relationship', 'Relationship to applicant', ['Self', 'Spouse', 'Child', 'Parent', 'Other']),
    select('sr22', 'SR-22 filing needed?', YES_NO),
    text('violations', 'Tickets or accidents in the last 3 years', hint='Date and type, or "none"'),
]

VEHICLE_FIELDS = [
    text('vin', 'VIN', True, hint='17 characters, on the dash or door sticker', pattern='[A-HJ-NPR-Za-hj-npr-z0-9]{17}', title='17 character VIN'),
    text('year-make-model', 'Year, make and model', True),
    select('use', 'Primary use', ['Commute', 'Pleasure', 'Business', 'Rideshare or delivery']),
    text('miles', 'Estimated annual miles', inputmode='numeric'),
    select('ownership', 'Ownership', ['Financed', 'Leased', 'Owned outright'], True),
    text('lienholder', 'Lienholder or lessor name and address', hint='Required when financed or leased'),
    select('coverage', 'Coverage wanted', ['Full coverage (liability, comprehensive, collision)', 'Liability only'], True),
    text('deductible', 'Preferred deductible', hint='$500 or $1,000 are most common'),
    select('dealer-purchase', 'Buying this vehicle at a dealership now?', YES_NO),
    text('dealer-name', 'Dealership name'),
]

AUTO_APP = {
    'key': 'auto',
    'file': 'apply/auto.html',
    'path': '/apply/auto',
    'form': 'application-auto',
    'title': 'Personal auto application',
    'intro': 'Everything a carrier needs to rate your auto policy. Add every licensed driver in the household and every vehicle you want covered. About 10 minutes.',
    'sections': [
        CONTACT,
        repeat('Drivers', 'Driver', DRIVER_FIELDS, 4, intro='List every licensed driver in the household, including anyone who will be excluded.'),
        repeat('Vehicles', 'Vehicle', VEHICLE_FIELDS, 4),
        PRIOR_INSURANCE,
        section('Documents (optional)', [
            upload('license-photo', 'Photo of driver\'s license or ID', 'JPG, PNG or PDF, under 4 MB'),
            upload('registration-photo', 'Vehicle registration or bill of sale', 'JPG, PNG or PDF, under 4 MB'),
        ], intro='Photos speed up the quote. You can also text them to the office after you submit.'),
        section('Anything else', [area('notes', 'Notes for the agent', 'Discounts you qualify for, payment preference, questions')]),
    ],
}

HOME_APP = {
    'key': 'home',
    'file': 'apply/home.html',
    'path': '/apply/home',
    'form': 'application-home',
    'title': 'Home, renters and condo application',
    'intro': 'Details about the property and the people living there. If you are closing on a home, include the closing date and your lender so the evidence of insurance is ready in time.',
    'sections': [
        CONTACT,
        section('Applicant', [
            text('dob', 'Date of birth', True, type='date'),
            ssn(),
            text('co-applicant', 'Co-applicant name and date of birth'),
            ssn('co-applicant-ssn', 'Co-applicant Social Security number'),
        ]),
        section('Property', [
            select('policy-type', 'Policy type', ['Homeowners', 'Renters', 'Condo', 'Landlord (rental property)'], True),
            text('property-address', 'Property address, if different from above'),
            text('year-built', 'Year built', inputmode='numeric'),
            text('square-feet', 'Living area in square feet', inputmode='numeric'),
            select('construction', 'Construction', ['Frame', 'Brick or masonry', 'Stucco', 'Other']),
            select('roof', 'Roof type', ['Composition shingle', 'Tile', 'Metal', 'Flat or built-up', 'Other']),
            text('roof-age', 'Roof age in years', inputmode='numeric'),
            select('occupancy', 'Occupancy', ['Owner occupied', 'Tenant occupied', 'Vacant', 'Seasonal']),
            text('purchase-price', 'Purchase price or estimated value', inputmode='numeric'),
            text('contents-value', 'Estimated value of belongings', inputmode='numeric'),
            select('protective', 'Protective devices', ['None', 'Smoke detectors only', 'Monitored alarm', 'Monitored alarm and sprinklers']),
            select('dogs', 'Dogs on the property?', YES_NO),
            text('dog-breeds', 'Dog breeds, if any'),
            select('pool', 'Swimming pool or trampoline?', YES_NO),
        ]),
        section('Mortgage and closing', [
            text('lender', 'Mortgage lender or landlord name'),
            text('lender-address', 'Lender address for the evidence of insurance'),
            text('loan-number', 'Loan number, if known'),
            text('closing-date', 'Closing or move-in date', type='date'),
        ]),
        section('Claims and prior insurance', [
            text('claims', 'Property claims in the last 5 years', hint='Date and type, or "none"'),
            text('prior-carrier', 'Current or most recent carrier'),
            text('desired-start', 'When do you need coverage to start?', True, type='date'),
            select('bundle-auto', 'Would you like an auto quote too?', YES_NO),
        ]),
        section('Anything else', [area('notes', 'Notes for the agent')]),
    ],
}

COMMERCIAL_VEHICLE_FIELDS = [
    text('vin', 'VIN', True, pattern='[A-HJ-NPR-Za-hj-npr-z0-9]{17}', title='17 character VIN'),
    text('year-make-model', 'Year, make and model', True),
    select('body-type', 'Body type', ['Pickup', 'Van', 'Box truck', 'Flatbed', 'Dump truck', 'Service truck', 'Sedan or SUV', 'Trailer', 'Other'], True),
    text('gvw', 'Gross vehicle weight (lbs)', inputmode='numeric'),
    text('value', 'Stated value', inputmode='numeric'),
    select('ownership', 'Ownership', ['Owned', 'Financed', 'Leased'], True),
    text('lienholder', 'Lienholder or lessor'),
    select('radius', 'Operating radius', ['Local, under 50 miles', 'Intermediate, 50 to 200 miles', 'Long haul, over 200 miles'], True),
    select('coverage', 'Coverage wanted', ['Liability and physical damage', 'Liability only'], True),
]

COMMERCIAL_DRIVER_FIELDS = [
    text('name', 'Full legal name', True),
    text('dob', 'Date of birth', True, type='date'),
    ssn(),
    text('license-number', 'Driver\'s license number'),
    select('license-state', 'License state', STATES, True),
    text('years-experience', 'Years of commercial driving experience', inputmode='numeric'),
    text('violations', 'Tickets or accidents in the last 3 years', hint='Date and type, or "none"'),
]

COMMERCIAL_AUTO_APP = {
    'key': 'commercial-auto',
    'file': 'apply/commercial-auto.html',
    'path': '/apply/commercial-auto',
    'form': 'application-commercial-auto',
    'title': 'Commercial auto application',
    'intro': 'For contractors, service businesses, delivery and any business that puts vehicles on the road. For tractors, semi trailers and for-hire trucking, use the trucking application instead.',
    'sections': [
        BUSINESS,
        section('Operations', [
            text('operations', 'What does the business do?', True, hint='Plumbing contractor, landscaping, food delivery, dealership'),
            text('employees', 'Number of employees', inputmode='numeric'),
            text('revenue', 'Annual revenue', inputmode='numeric'),
            select('hired-nonowned', 'Need hired and non-owned auto coverage?', YES_NO, hint='Employees driving their own vehicles for work, or rented vehicles'),
            text('liability-limit', 'Liability limit required by contracts, if any', hint='$1,000,000 combined single limit is common'),
            text('certificate-holders', 'Certificate holders', hint='Who needs a certificate of insurance'),
        ]),
        repeat('Vehicles', 'Vehicle', COMMERCIAL_VEHICLE_FIELDS, 6),
        repeat('Drivers', 'Driver', COMMERCIAL_DRIVER_FIELDS, 6),
        section('Prior insurance', [
            text('prior-carrier', 'Current or most recent carrier'),
            text('prior-premium', 'Current annual premium', inputmode='numeric'),
            text('prior-expiration', 'Policy expiration date', type='date'),
            text('claims', 'Claims in the last 3 years', hint='Date, type and amount, or "none"'),
            text('desired-start', 'When do you need coverage to start?', True, type='date'),
            upload('loss-runs', 'Loss runs (optional)', 'PDF under 4 MB. Carriers ask for 3 years.'),
        ]),
        section('Anything else', [area('notes', 'Notes for the agent')]),
    ],
}

POWER_UNIT_FIELDS = [
    text('vin', 'VIN', True, pattern='[A-HJ-NPR-Za-hj-npr-z0-9]{17}', title='17 character VIN'),
    text('year-make-model', 'Year, make and model', True),
    select('unit-type', 'Unit type', ['Tractor (sleeper)', 'Tractor (day cab)', 'Straight truck', 'Box truck', 'Dump truck', 'Tow truck', 'Other'], True),
    text('gvw', 'GVW or GCW (lbs)', inputmode='numeric'),
    text('value', 'Stated value', True, inputmode='numeric'),
    select('ownership', 'Ownership', ['Owned', 'Financed', 'Leased'], True),
    text('lienholder', 'Lienholder or lessor'),
    select('coverage', 'Coverage wanted', ['Liability and physical damage', 'Liability only', 'Physical damage only (leased on)'], True),
]

TRAILER_FIELDS = [
    text('vin', 'VIN', pattern='[A-HJ-NPR-Za-hj-npr-z0-9]{17}', title='17 character VIN'),
    text('year-make', 'Year and make'),
    select('trailer-type', 'Trailer type', ['Dry van', 'Reefer', 'Flatbed', 'Step deck', 'Lowboy', 'Tanker', 'Dump', 'Car hauler', 'Other']),
    text('value', 'Stated value', inputmode='numeric'),
    select('ownership', 'Ownership', ['Owned', 'Financed', 'Leased', 'Trailer interchange']),
]

TRUCK_DRIVER_FIELDS = [
    text('name', 'Full legal name', True),
    text('dob', 'Date of birth', True, type='date'),
    ssn(),
    text('cdl-number', 'CDL number', True),
    select('cdl-state', 'CDL state', STATES, True),
    text('cdl-years', 'Years holding a CDL', True, inputmode='numeric'),
    text('hire-date', 'Date of hire', type='date'),
    text('violations', 'Moving violations or accidents in the last 3 years', hint='Date and type, or "none"'),
]

TRUCKING_APP = {
    'key': 'trucking',
    'file': 'apply/trucking.html',
    'path': '/apply/trucking',
    'form': 'application-trucking',
    'title': 'Commercial trucking application',
    'intro': 'For motor carriers and owner-operators. Have your USDOT number, equipment list and driver CDLs ready. Loss runs and a copy of your MCS-150 speed up the quote.',
    'sections': [
        BUSINESS,
        section('Authority and operations', [
            text('usdot', 'USDOT number', True, inputmode='numeric'),
            text('mc', 'MC number', hint='Leave blank if you have not applied'),
            select('authority-status', 'Operating authority', ['Active', 'Pending (new venture)', 'Leased onto another carrier', 'Intrastate only'], True),
            text('authority-date', 'Date authority was granted or applied for', type='date'),
            select('operation', 'Type of operation', ['For hire, general freight', 'For hire, specialized', 'Private carrier (own goods)', 'Owner-operator leased on', 'Hot shot', 'Auto hauler', 'Dump or aggregate', 'Other'], True),
            text('commodities', 'Commodities hauled', True, hint='General freight, produce, steel, vehicles, hazmat'),
            select('hazmat', 'Hazardous materials?', YES_NO),
            select('radius', 'Operating radius', ['Local, under 100 miles', 'Regional, 100 to 500 miles', 'Long haul, over 500 miles'], True),
            text('states', 'States you operate in', True),
            text('annual-miles', 'Total annual miles, all units', inputmode='numeric'),
            text('annual-revenue', 'Annual gross revenue', inputmode='numeric'),
            text('leased-carrier', 'If leased on, name of the motor carrier'),
        ]),
        section('Coverage requested', [
            select('liability-limit', 'Auto liability limit', ['$750,000', '$1,000,000', '$2,000,000', 'Not sure'], True),
            select('cargo', 'Motor truck cargo', ['$100,000', '$250,000', 'Not needed', 'Not sure']),
            select('general-liability', 'General liability', ['$1,000,000 / $2,000,000', 'Not needed', 'Not sure']),
            select('physical-damage', 'Physical damage on equipment', YES_NO),
            select('ntl', 'Non-trucking liability (bobtail)', ['Not needed', 'Needed (leased on)']),
            select('trailer-interchange', 'Trailer interchange', ['Not needed', 'Needed']),
            select('occ-acc', 'Occupational accident for owner-operators', ['Not needed', 'Needed']),
            text('filings', 'Filings required', hint='MCS-90, BMC-91X, Form E, Form H, UIIA'),
            text('shipper-requirements', 'Shipper or broker contract requirements', hint='Limits, additional insureds, waiver of subrogation'),
        ]),
        repeat('Power units', 'Unit', POWER_UNIT_FIELDS, 6),
        repeat('Trailers', 'Trailer', TRAILER_FIELDS, 6),
        repeat('Drivers', 'Driver', TRUCK_DRIVER_FIELDS, 6, intro='Every driver with access to the equipment. Carriers will run MVRs.'),
        section('Loss history and prior insurance', [
            text('prior-carrier', 'Current or most recent carrier'),
            text('prior-premium', 'Current annual premium', inputmode='numeric'),
            text('prior-expiration', 'Policy expiration date', type='date'),
            text('claims', 'Claims in the last 3 years', hint='Date, type and amount, or "none"'),
            text('desired-start', 'When do you need coverage to start?', True, type='date'),
            upload('loss-runs', 'Loss runs, 3 years (optional)', 'PDF under 4 MB'),
            upload('mcs150', 'MCS-150 or authority letter (optional)', 'PDF or image under 4 MB'),
        ]),
        section('Anything else', [area('notes', 'Notes for the agent', 'Safety program, ELD, cameras, driver training, anything that helps your rate')]),
    ],
}

GL_APP = {
    'key': 'general-liability',
    'file': 'apply/general-liability.html',
    'path': '/apply/general-liability',
    'form': 'application-general-liability',
    'title': 'General liability application',
    'intro': 'Premises and operations coverage for small businesses, with certificates for landlords and customers.',
    'sections': [
        BUSINESS,
        section('Operations', [
            text('operations', 'Describe the work you do', True),
            select('location-type', 'Premises', ['Home based', 'Leased office or shop', 'Owned building', 'Job sites only', 'Retail storefront'], True),
            text('employees', 'Number of employees', inputmode='numeric'),
            text('payroll', 'Annual payroll', inputmode='numeric'),
            text('revenue', 'Annual revenue', True, inputmode='numeric'),
            text('subcontractors', 'Annual cost of subcontractors', inputmode='numeric'),
            select('limit', 'Limit requested', ['$1,000,000 / $2,000,000', '$2,000,000 / $4,000,000', 'Not sure'], True),
            text('certificate-holders', 'Certificate holders and additional insureds', hint='Landlord, general contractor, city'),
            select('other-coverage', 'Also quote', ['Nothing else', 'Commercial property or BOP', 'Workers compensation', 'Commercial auto', 'Professional liability']),
        ]),
        section('Prior insurance', [
            text('prior-carrier', 'Current or most recent carrier'),
            text('claims', 'Liability claims in the last 5 years', hint='Date, type and amount, or "none"'),
            text('desired-start', 'When do you need coverage to start?', True, type='date'),
        ]),
        section('Anything else', [area('notes', 'Notes for the agent')]),
    ],
}

APPLICATIONS = [AUTO_APP, HOME_APP, COMMERCIAL_AUTO_APP, TRUCKING_APP, GL_APP]


# ------------------------------------------------------------------ rendering

def _attrs(extra):
    return ''.join(f' {k}="{escape(str(v), quote=True)}"' for k, v in extra.items())


def render_field(field, prefix, required_ok):
    """prefix is '' for plain sections or 'driver-2-' for repeated rows."""
    name = prefix + field['name']
    fid = 'f-' + name
    required = ' required' if (field.get('required') and required_ok) else ''
    label = escape(field['label'])
    hint = f' <span class="hint">{escape(field["hint"])}</span>' if field.get('hint') else ''
    kind = field['type']
    if kind == 'select':
        options = ''.join(f'<option>{escape(o)}</option>' for o in field['options'])
        control = f'<select id="{fid}" name="{name}"{required}>{options}</select>'
    elif kind == 'textarea':
        control = f'<textarea id="{fid}" name="{name}" rows="4"{required}></textarea>'
    elif kind == 'file':
        control = f'<input id="{fid}" name="{name}" type="file" accept="image/*,.pdf">'
    else:
        attrs = dict(field.get('attrs') or {})
        attrs.setdefault('type', 'text')
        control = f'<input id="{fid}" name="{name}"{_attrs(attrs)}{required}>'
    wide = ' field-wide' if kind in ('textarea',) else ''
    return f'<div class="field{wide}"><label for="{fid}">{label}{hint}</label>{control}</div>'


def render_section(sec):
    intro = f'<p class="app-intro">{escape(sec["intro"])}</p>' if sec.get('intro') else ''
    if not sec['repeat']:
        fields = ''.join(render_field(f, '', True) for f in sec['fields'])
        return f'<fieldset class="app-section"><legend>{escape(sec["title"])}</legend>{intro}<div class="app-grid">{fields}</div></fieldset>'

    item = sec['repeat']['item']
    slug = item.lower()
    rows = []
    for i in range(1, sec['repeat']['count'] + 1):
        hidden = '' if i == 1 else ' js-hidden'
        fields = ''.join(render_field(f, f'{slug}-{i}-', i == 1) for f in sec['fields'])
        remove = '' if i == 1 else f'<button type="button" class="btn btn-outline btn-sm js-only" data-remove>Remove {escape(item.lower())} {i}</button>'
        rows.append(f'<div class="app-row{hidden}" data-row><h3>{escape(item)} {i}</h3><div class="app-grid">{fields}</div>{remove}</div>')
    add = f'<button type="button" class="btn btn-outline js-only" data-add>Add another {escape(item.lower())}</button>'
    return f'<fieldset class="app-section" data-repeat="{slug}"><legend>{escape(sec["title"])}</legend>{intro}{"".join(rows)}{add}</fieldset>'


def render_application(app, phone, phone_href):
    sections = ''.join(render_section(s) for s in app['sections'])
    return f'''<section class="page-head"><div class="wrap"><p class="eyebrow">APPLICATION</p><h1>{escape(app["title"])}</h1><p>{escape(app["intro"])}</p></div></section>
<section class="section"><div class="wrap app-wrap">
  <form class="app-form" name="{app["form"]}" method="POST" action="{INTAKE_URL}" enctype="multipart/form-data" data-intake data-success="/thank-you">
    <input type="hidden" name="form-name" value="{app["form"]}">
    <p class="hidden" aria-hidden="true"><label>Company <input name="company" tabindex="-1" autocomplete="off"></label></p>
    {sections}
    <div class="app-submit">
      <p class="form-status" role="status" aria-live="polite"></p>
      <button class="btn btn-accent" type="submit">Submit application</button>
      <p class="consent">By submitting you confirm the information is accurate to the best of your knowledge and agree that Insurance Capitol may call, text or email you about this application. Submitting does not bind coverage; a policy is in force only when a carrier issues it. Your application is sent over an encrypted connection to our secure system; Social Security numbers are stored encrypted. Do not include payment card numbers. <a href="/privacy">Privacy policy</a>.</p>
    </div>
  </form>
  <aside class="app-aside">
    <h2>Rather talk it through?</h2>
    <p>Call or text <a href="{phone_href}">{phone}</a> and we will take the application over the phone. Hablamos español.</p>
    <h2>What happens next</h2>
    <ol>
      <li>Your application is delivered to our office the moment you submit, over an encrypted connection.</li>
      <li>We rate it with the carriers that fit and call you with options, usually the same business day.</li>
      <li>You choose, make the down payment with the carrier, and we send proof of insurance to you and your lender.</li>
    </ol>
  </aside>
</div></section>'''


def render_index(phone_href, phone):
    cards = [
        ('/apply/auto', 'Personal auto', 'Cars, trucks and SUVs for you and your household. SR-22 and foreign license welcome.'),
        ('/apply/home', 'Home, renters and condo', 'Where you live and what is inside it, with lender evidence of insurance handled.'),
        ('/apply/commercial-auto', 'Commercial auto', 'Work trucks, vans and fleets for contractors, delivery and service businesses.'),
        ('/apply/trucking', 'Commercial trucking', 'Motor carriers and owner-operators: liability, cargo, physical damage and filings.'),
        ('/apply/general-liability', 'General liability', 'Premises and operations coverage with certificates for landlords and customers.'),
    ]
    items = ''.join(
        f'<a class="coverage-card" href="{href}"><h3>{escape(t)}</h3><p>{escape(d)}</p><span class="card-link">Start application</span></a>'
        for href, t, d in cards
    )
    return f'''<section class="page-head"><div class="wrap"><p class="eyebrow">APPLY</p><h1>Start an application</h1><p>Pick the coverage you need. Each application asks only what a carrier needs to rate it, and goes straight to our office when you submit. Need a quick estimate first? <a href="/#quote">Request a quote</a> instead.</p></div></section>
<section class="section"><div class="wrap"><div class="grid-3 app-cards">{items}</div>
<p class="small mt-md">Prefer paper or a phone call? Call <a href="{phone_href}">{phone}</a> and we will take it down for you.</p></div></section>'''
