(() => {
  'use strict';
  document.documentElement.classList.add('js');

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

  // Repeatable application rows: every row exists in the HTML; rows after the
  // first are hidden until added. Removing a row clears it and hides it again.
  document.querySelectorAll('[data-repeat]').forEach(group => {
    const rows = [...group.querySelectorAll('[data-row]')];
    const add = group.querySelector('[data-add]');
    const refresh = () => { add.hidden = rows.every(row => !row.classList.contains('js-hidden')); };
    add.addEventListener('click', () => {
      const next = rows.find(row => row.classList.contains('js-hidden'));
      if (!next) return;
      next.classList.remove('js-hidden');
      next.querySelector('input, select, textarea').focus();
      refresh();
    });
    rows.forEach(row => {
      const remove = row.querySelector('[data-remove]');
      if (!remove) return;
      remove.addEventListener('click', () => {
        row.querySelectorAll('input, select, textarea').forEach(field => {
          if (field.tagName === 'SELECT') field.selectedIndex = 0; else field.value = '';
        });
        row.classList.add('js-hidden');
        refresh();
        add.focus();
      });
    });
    refresh();
  });

  // Sections shown only when a coverage choice is checked (commercial details on the quote form).
  document.querySelectorAll('[data-show-when]').forEach(block => {
    const form = block.closest('form');
    const value = block.getAttribute('data-show-when');
    const sync = () => {
      const on = [...form.querySelectorAll('[name="coverage"]')].some(input => input.checked && input.value === value);
      block.classList.toggle('js-hidden', !on);
      block.querySelectorAll('input, select, textarea').forEach(field => { field.disabled = !on; });
    };
    form.addEventListener('change', sync);
    sync();
  });

  // Every form posts to the RunTorque intake endpoint (data-intake), which stores
  // the request, emails the office and answers with JSON.
  document.querySelectorAll('form[data-intake]').forEach(form => {
    const status = form.querySelector('.form-status');
    const submit = form.querySelector('button[type="submit"]');
    const method = form.querySelector('[name="contact-preference"]');
    const email = form.querySelector('[name="email"]');
    const choices = [...form.querySelectorAll('[name="coverage"]')];
    const target = form.getAttribute('action');
    const success = form.getAttribute('data-success');

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
        const response = await fetch(target, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
        const data = await response.json().catch(() => ({}));
        if (!response.ok || !data.ok) throw new Error(data.error || 'Submission failed');
        location.assign(success);
      } catch (error) {
        const detail = error.message && error.message !== 'Submission failed' ? ` ${error.message}.` : '';
        status.textContent = `Your request could not be sent.${detail} Please try again or call 915-760-4411.`;
        submit.disabled = false;
        submit.textContent = original;
      } finally { form.removeAttribute('aria-busy'); }
    });
  });
})();
