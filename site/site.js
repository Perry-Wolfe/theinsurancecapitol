(() => {
  'use strict';
  const button = document.querySelector('.menu-btn');
  const nav = document.getElementById('nav');
  function closeMenu() {
    if (!nav || !button) return;
    nav.classList.remove('open');
    button.setAttribute('aria-expanded', 'false');
    button.textContent = 'Menu';
  }
  if (button && nav) {
    button.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      button.setAttribute('aria-expanded', String(open));
      button.textContent = open ? 'Close' : 'Menu';
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); button.focus(); }
    });
    document.addEventListener('click', event => { if (!event.target.closest('.top')) closeMenu(); });
    matchMedia('(min-width: 1051px)').addEventListener('change', closeMenu);
  }
  document.querySelectorAll('[data-year]').forEach(el => { el.textContent = String(new Date().getFullYear()); });
  document.querySelectorAll('form[data-netlify]').forEach(form => {
    const status = form.querySelector('.form-status');
    const submit = form.querySelector('button[type="submit"]');
    const method = form.querySelector('[name="contact-preference"]');
    const email = form.querySelector('[name="email"]');
    const choices = [...form.querySelectorAll('[name="coverage"]')];
    const validateChoices = () => {
      if (choices.length) choices[0].setCustomValidity(choices.some(input => input.checked) ? '' : 'Please select at least one coverage type.');
    };
    choices.forEach(input => input.addEventListener('change', validateChoices));
    validateChoices();
    if (method && email) method.addEventListener('change', () => { email.required = method.value === 'Email'; });
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      if (['localhost', '127.0.0.1'].includes(location.hostname) || location.protocol === 'file:') {
        status.textContent = 'This preview cannot deliver requests. Please call the agency, or submit on the live website.';
        return;
      }
      const original = submit.textContent;
      submit.disabled = true;
      submit.textContent = 'Sending…';
      status.textContent = '';
      form.setAttribute('aria-busy', 'true');
      try {
        const body = new URLSearchParams();
        new FormData(form).forEach((value, key) => body.append(key, String(value)));
        const response = await fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: body.toString() });
        if (!response.ok) throw new Error('Submission failed');
        location.assign(form.getAttribute('action'));
      } catch {
        status.textContent = 'Your request could not be sent. Please try again or call 915-760-4411.';
        submit.disabled = false;
        submit.textContent = original;
      } finally { form.removeAttribute('aria-busy'); }
    });
  });
})();
