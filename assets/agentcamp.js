(function () {
  'use strict';
  var form = document.getElementById('acForm');
  if (!form) return;
  var button = document.getElementById('acBtn');
  var error = document.getElementById('acError');
  var submitting = false;
  var requestId = '';
  var lastPayload = '';
  var storageKey = 'agentcamp_submission';

  function val(id) { return (document.getElementById(id).value || '').trim(); }
  function mark(id, bad) { document.getElementById(id).closest('.ac-field').classList.toggle('err', !!bad); }
  function analytics(result) {
    try {
      if (window.JZAnalytics) window.JZAnalytics.trackButton('AgentCamp报名', 'AgentCamp·报名表', { submission_result: result });
    } catch (_) {}
  }
  function newId() {
    if (window.crypto.randomUUID) return window.crypto.randomUUID();
    var bytes = new Uint8Array(16);
    window.crypto.getRandomValues(bytes);
    bytes[6] = (bytes[6] & 15) | 64;
    bytes[8] = (bytes[8] & 63) | 128;
    var hex = Array.from(bytes, function (b) { return b.toString(16).padStart(2, '0'); }).join('');
    return hex.slice(0, 8) + '-' + hex.slice(8, 12) + '-' + hex.slice(12, 16) + '-' + hex.slice(16, 20) + '-' + hex.slice(20);
  }

  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    if (submitting) return;
    error.hidden = true;
    var bad = false;
    ['f-name', 'f-company', 'f-task'].forEach(function (id) {
      var invalid = !val(id); mark(id, invalid); bad = bad || invalid;
    });
    var contact = val('f-contact');
    var contactValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(contact) || /^\+?[\d ()-]{7,25}$/.test(contact) && contact.replace(/\D/g, '').length >= 7;
    mark('f-contact', !contactValid); bad = bad || !contactValid;
    var agree = document.getElementById('f-agree').checked;
    document.getElementById('acConsent').classList.toggle('err', !agree); bad = bad || !agree;
    if (bad || !form.checkValidity()) {
      var first = form.querySelector('.err input,.err textarea,.ac-consent.err input,:invalid');
      if (first) first.focus();
      return;
    }
    var payload = JSON.stringify({ name: val('f-name'), company: val('f-company'), title: val('f-title'),
      contact: contact, city: val('f-city'), when: val('f-when'), task: val('f-task'), data: val('f-data'), agree: true, page: 'agentcamp' });
    submitting = true;
    button.disabled = true;
    form.setAttribute('aria-busy', 'true');
    var controller = new AbortController();
    var timeout = setTimeout(function () { controller.abort(); }, 35000);
    try {
      // Only the random key is persisted; never retain form contents in browser storage.
      if (!requestId || lastPayload !== payload) {
        var saved;
        try { saved = JSON.parse(sessionStorage.getItem(storageKey) || 'null'); } catch (_) {}
        requestId = !lastPayload && saved && /^[0-9a-f-]{36}$/i.test(saved.id) && Date.now() - saved.at < 86400000 ? saved.id : newId();
        lastPayload = payload;
        try { sessionStorage.setItem(storageKey, JSON.stringify({ id: requestId, at: Date.now() })); } catch (_) {}
      }
      analytics('attempt');
      var response = await fetch('/api/agentcamp/applications', {
        method: 'POST', headers: { 'Content-Type': 'application/json', 'Idempotency-Key': requestId },
        body: payload, signal: controller.signal
      });
      var result;
      try { result = await response.json(); } catch (_) {}
      if (!response.ok || !result || result.ok !== true || !result.submissionId) {
        if (response.status === 409) {
          requestId = ''; lastPayload = '';
          try { sessionStorage.removeItem(storageKey); } catch (_) {}
          throw new Error('内容已更改，请再次点击提交预约。');
        }
        if (response.status === 429) throw new Error('提交较频繁，请稍等一分钟再试。');
        if (response.status === 400) throw new Error('请检查填写内容和联系方式，再试一次。');
        throw new Error('暂未确认提交结果，请稍后重试，已填内容会保留。');
      }
      form.classList.add('sent');
      analytics('success');
      try { sessionStorage.removeItem(storageKey); } catch (_) {}
      form.reset();
      form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (failure) {
      error.textContent = failure instanceof Error && failure.message && !['AbortError', 'TypeError'].includes(failure.name)
        ? failure.message : '暂未确认提交结果，请稍后重试，已填内容会保留。';
      error.hidden = false;
      analytics('failure');
    } finally {
      clearTimeout(timeout);
      submitting = false;
      button.disabled = false;
      form.removeAttribute('aria-busy');
    }
  });
})();
