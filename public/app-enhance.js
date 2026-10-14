/**
 * BidTrace UI Enhancement Layer (Phases 1-3)
 * Non-breaking: patches existing inline dashboard functions, adds toasts,
 * receipt persistence, wallet fixes, guided mode, live helpers.
 * Loaded AFTER bidtrace_web3.js, BEFORE inline <script> runs enhancements on DOMContentLoaded.
 */
(function () {
  'use strict';

  // --- 0. Back-compat alias (fixes index.html:1156 bug) ---
  try {
    if (window.BidTraceWeb3 && !window.bidtraceWeb3) window.bidtraceWeb3 = window.BidTraceWeb3;
    if (window.bidtraceWeb3 && !window.BidTraceWeb3) window.BidTraceWeb3 = window.bidtraceWeb3;
  } catch (e) {}

  const CFG = window.BidTraceConfig || {};
  const LS_RECEIPTS = (CFG.storageKeys && CFG.storageKeys.receipts) || 'bidtrace_receipts_v1';
  const LS_MODE = (CFG.storageKeys && CFG.storageKeys.mode) || 'bidtrace_ui_mode';

  // --- 1. Toast system (replaces alert/confirm) ---
  function ensureToastRoot() {
    let root = document.getElementById('bt-toast-root');
    if (!root) {
      root = document.createElement('div');
      root.id = 'bt-toast-root';
      root.setAttribute('aria-live', 'polite');
      document.body.appendChild(root);
    }
    return root;
  }

  function toast(msg, type) {
    type = type || 'info';
    const root = ensureToastRoot();
    const el = document.createElement('div');
    el.className = 'bt-toast bt-toast-' + type;
    el.setAttribute('role', 'status');
    const dot = document.createElement('span');
    dot.className = 'bt-toast-dot';
    const txt = document.createElement('span');
    txt.textContent = msg; // XSS-safe: never innerHTML user data
    el.appendChild(dot);
    el.appendChild(txt);
    root.appendChild(el);
    requestAnimationFrame(function () { el.classList.add('show'); });
    setTimeout(function () {
      el.classList.remove('show');
      setTimeout(function () { el.remove(); }, 350);
    }, 4200);
    // Mirror into activity feeds (sanitized)
    try { if (window.logMessage) window.logMessage(msg, type === 'danger' ? 'error' : type); } catch (e) {}
  }

  // Non-blocking confirm dialog (replaces window.confirm for reset)
  function confirmDialog(message) {
    return new Promise(function (resolve) {
      const overlay = document.createElement('div');
      overlay.className = 'bt-confirm-overlay';
      overlay.innerHTML = '';
      const card = document.createElement('div');
      card.className = 'bt-confirm-card modal-animate';
      card.setAttribute('role', 'alertdialog');
      const title = document.createElement('div');
      title.className = 'bt-confirm-title';
      title.textContent = 'Please confirm';
      const body = document.createElement('p');
      body.className = 'bt-confirm-body';
      body.textContent = message;
      const row = document.createElement('div');
      row.className = 'bt-confirm-row';
      const cancel = document.createElement('button');
      cancel.className = 'bt-btn bt-btn-ghost';
      cancel.textContent = 'Cancel';
      const ok = document.createElement('button');
      ok.className = 'bt-btn bt-btn-danger';
      ok.textContent = 'Reset & start fresh';
      cancel.onclick = function () { overlay.remove(); resolve(false); };
      ok.onclick = function () { overlay.remove(); resolve(true); };
      overlay.onclick = function (e) { if (e.target === overlay) { overlay.remove(); resolve(false); } };
      row.appendChild(cancel); row.appendChild(ok);
      card.appendChild(title); card.appendChild(body); card.appendChild(row);
      overlay.appendChild(card);
      document.body.appendChild(overlay);
      ok.focus();
    });
  }

  // Patch native alert -> toast (keeps inline calls working, no blocking)
  try {
    const nativeAlert = window.alert.bind(window);
    window.alert = function (msg) {
      try { toast(String(msg), 'warning'); } catch (e) { nativeAlert(msg); }
    };
  } catch (e) {}

  // --- 2. Receipt persistence (fixes reload-bricks-reveal) ---
  function loadPersistedReceipts() {
    try {
      const raw = localStorage.getItem(LS_RECEIPTS);
      if (!raw) return [];
      const arr = JSON.parse(raw);
      return Array.isArray(arr) ? arr : [];
    } catch (e) { return []; }
  }
  function persistReceipts(arr) {
    try { localStorage.setItem(LS_RECEIPTS, JSON.stringify(arr || [])); } catch (e) {}
  }

  // --- 3. Sanitized logger (patches XSS via innerHTML in logMessage) ---
  function patchLogger() {
    if (!window.logMessage || window.logMessage.__btPatched) return;
    const orig = window.logMessage;
    window.logMessage = function (msg, type) {
      try {
        const logs1 = document.getElementById('demo-console-logs');
        const logs2 = document.getElementById('devnet-web3-logs');
        const d = document.createElement('div');
        if (type === 'error' || type === 'danger') d.className = 'text-rose-400 font-semibold';
        else if (type === 'success') d.className = 'text-emerald-400 font-semibold';
        else if (type === 'warning') d.className = 'text-amber-400 font-semibold';
        else d.className = 'text-slate-300';
        const ts = document.createElement('span');
        ts.className = 'opacity-60';
        ts.textContent = '[' + new Date().toISOString().slice(14, 19) + '] ';
        const body = document.createElement('span');
        body.textContent = String(msg);
        d.appendChild(ts); d.appendChild(body);
        if (logs1) logs1.prepend(d.cloneNode(true));
        if (logs2) logs2.prepend(d);
      } catch (e) { orig(msg, type); }
    };
    window.logMessage.__btPatched = true;
  }

  // --- 4. Guided / Advanced mode ---
  function setMode(mode) {
    try { localStorage.setItem(LS_MODE, mode); } catch (e) {}
    document.body.setAttribute('data-bt-mode', mode);
    const guidedBtn = document.getElementById('bt-mode-guided');
    const advBtn = document.getElementById('bt-mode-advanced');
    [guidedBtn, advBtn].forEach(function (b) { if (b) b.classList.remove('bt-mode-active'); });
    if (mode === 'guided' && guidedBtn) guidedBtn.classList.add('bt-mode-active');
    if (mode === 'advanced' && advBtn) advBtn.classList.add('bt-mode-active');
    // In guided mode, collapse technical drawers; in advanced, expand
    document.querySelectorAll('[data-bt-advanced]').forEach(function (el) {
      if (mode === 'guided') el.classList.add('bt-collapsed-hint');
      else el.classList.remove('bt-collapsed-hint');
    });
    const hint = document.getElementById('bt-mode-hint');
    if (hint) {
      hint.textContent = mode === 'guided'
        ? 'Guided: follow steps 1–5. Technical details are tucked away.'
        : 'Advanced: all portals, hashes, slots and OCDS feeds visible.';
    }
  }

  // --- 5. Tender templates ---
  function applyTemplate(id) {
    const t = (CFG.templates || []).find(function (x) { return x.id === id; });
    if (!t) return;
    const set = function (elId, val) { const el = document.getElementById(elId); if (el) el.value = val; };
    set('buyer-tech-weight', t.techWeight);
    set('buyer-fin-weight', t.finWeight);
    set('buyer-min-score', t.minScore);
    set('buyer-bond-amount', t.bond);
    toast('Template applied: ' + t.label, 'success');
  }

  // --- 6. Live tech-hash preview (uses SHA-256, honest "computed in browser") ---
  async function updateTechHashPreview() {
    const specsEl = document.getElementById('bidder-tech-specs');
    const out = document.getElementById('bidder-tech-hash-display');
    if (!specsEl || !out) return;
    const text = specsEl.value || '';
    try {
      const bytes = new TextEncoder().encode(text);
      let hex = '';
      if (window.crypto && window.crypto.subtle) {
        const buf = await window.crypto.subtle.digest('SHA-256', bytes);
        hex = Array.from(new Uint8Array(buf)).map(function (b) { return b.toString(16).padStart(2, '0'); }).join('');
      }
      out.textContent = hex ? ('sha256:' + hex.slice(0, 16) + '…') : 'Auto-computed in browser';
      out.title = hex || '';
    } catch (e) {}
  }

  // --- 7. Wallet balance (fixes never-updated #wallet-balance-display) ---
  async function refreshWalletBalance() {
    const balEl = document.getElementById('wallet-balance-display');
    if (!balEl) return;
    try {
      const mgr = (window.BidTraceWeb3 && window.BidTraceWeb3.walletManager) ||
                  (window.bidtraceWeb3 && window.bidtraceWeb3.walletManager);
      if (mgr && mgr.isConnected && mgr.publicKey) {
        const bal = await mgr.getBalance();
        balEl.textContent = Number(bal || 0).toFixed(2) + ' SOL (devnet)';
      }
    } catch (e) {}
  }

  // --- 8. Devnet panel: populate dead #devnet-tx-list-portal ---
  async function refreshDevnetPanel() {
    const box = document.getElementById('devnet-tx-list-portal');
    if (!box || box.__btFilled) return;
    try {
      const res = await fetch('/api/devnet/status');
      const data = await res.json();
      box.__btFilled = true;
      box.innerHTML = '';
      const mk = function (k, v, cls) {
        const row = document.createElement('div');
        row.className = 'p-2.5 rounded bg-slate-950 border border-slate-800 flex items-center justify-between text-[11px]';
        const a = document.createElement('span'); a.className = 'text-slate-400'; a.textContent = k;
        const b = document.createElement('span'); b.className = 'mono ' + (cls || 'text-slate-200'); b.textContent = v;
        row.appendChild(a); row.appendChild(b); return row;
      };
      box.appendChild(mk('Cluster', data.cluster || 'devnet', 'text-purple-300'));
      box.appendChild(mk('Program', (data.program_id || CFG.programId || '').slice(0, 12) + '…', 'text-cyan-300'));
      box.appendChild(mk('Devnet slot', data.devnet_slot != null ? String(data.devnet_slot) : 'offline (relayer mode)', 'text-slate-200'));
      const note = document.createElement('div');
      note.className = 'text-[11px] text-slate-500 p-1';
      note.textContent = 'Dashboard flows run through the gas-sponsored relayer. Direct on-chain writes use Phantom / Devnet Keypair in BidTraceWeb3.';
      box.appendChild(note);
    } catch (e) {}
  }

  // --- 9. Rubric sliders affordance + trimmed-mean hint ---
  function hookRubrics() {
    ['rubric-1', 'rubric-2', 'rubric-3', 'rubric-4', 'rubric-5'].forEach(function (id) {
      const el = document.getElementById(id);
      if (el && !el.__btHooked) {
        el.__btHooked = true;
        el.addEventListener('input', function () {
          if (window.updateRubricTotal) try { window.updateRubricTotal(); } catch (e) {}
        });
      }
    });
  }

  // --- 10. Boot ---
  function boot() {
    patchLogger();
    // alias again after inline script defines globals
    try {
      if (window.BidTraceWeb3 && !window.bidtraceWeb3) window.bidtraceWeb3 = window.BidTraceWeb3;
    } catch (e) {}

    // Restore receipts into global localReceipts (inline script owns the var)
    try {
      const saved = loadPersistedReceipts();
      if (saved.length && typeof localReceipts !== 'undefined' && localReceipts.length === 0) {
        saved.forEach(function (r) { localReceipts.push(r); });
        const cnt = document.getElementById('bidder-receipt-count');
        if (cnt) cnt.textContent = localReceipts.length + ' Saved (restored)';
      }
      // Wrap push paths: poll for changes and persist (covers commitDualBid/demo/storyboard)
      setInterval(function () {
        try {
          if (typeof localReceipts !== 'undefined' && localReceipts.length) persistReceipts(localReceipts);
        } catch (e) {}
      }, 2000);
      // Persist on reset paths too
      const origReset = window.resetGlobalProtocol;
      if (origReset && !origReset.__btWrapped) {
        const wrapped = async function () {
          const ok = await confirmDialog('Reset all relayer state and start fresh? Receipts saved in this browser will be cleared.');
          if (!ok) return;
          await origReset.__btOrig ? origReset.__btOrig() : null;
        };
        // Simpler: replace global with confirming version that calls API directly
        window.resetGlobalProtocol = async function () {
          const ok = await confirmDialog('Reset all relayer state and start fresh?');
          if (!ok) return;
          await fetch('/api/reset', { method: 'POST' });
          try { localReceipts = []; } catch (e) {}
          persistReceipts([]);
          try { window.currentStoryboardStep = 0; } catch (e) {}
          if (window.setStoryboardStepUI) window.setStoryboardStepUI(0);
          toast('Protocol state reset.', 'warning');
          if (window.refreshStatus) window.refreshStatus();
        };
        window.resetGlobalProtocol.__btWrapped = true;
      }
    } catch (e) {}

    // Mode
    let mode = 'guided';
    try { mode = localStorage.getItem(LS_MODE) || 'guided'; } catch (e) {}
    setMode(mode === 'advanced' ? 'advanced' : 'guided');

    // Helpers exposure
    window.BidTraceUI = {
      toast: toast, confirmDialog: confirmDialog,
      setMode: setMode, applyTemplate: applyTemplate,
      refreshWalletBalance: refreshWalletBalance,
      saveReceipts: function () { try { persistReceipts(localReceipts); } catch (e) {} }
    };

    // Listeners
    const specsEl = document.getElementById('bidder-tech-specs');
    if (specsEl && !specsEl.__btHooked) {
      specsEl.__btHooked = true;
      specsEl.addEventListener('input', updateTechHashPreview);
      updateTechHashPreview();
    }
    hookRubrics();
    setInterval(refreshWalletBalance, 5000);
    refreshWalletBalance();
    refreshDevnetPanel();
    setInterval(refreshDevnetPanel, 15000);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
