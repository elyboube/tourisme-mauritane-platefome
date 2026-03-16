/* =============================================
   MAURITANIE TOURISME — JavaScript Principal
   ============================================= */

'use strict';

// ─── UTILITAIRES ──────────────────────────────
function getCookie(name) {
  const v = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
  return v ? v[2] : null;
}

function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  const icons = { success: 'check-circle', danger: 'times-circle', warning: 'exclamation-triangle', info: 'info-circle' };
  toast.className = `toast align-items-center text-bg-${type} border-0 show mb-2`;
  toast.setAttribute('role', 'alert');
  toast.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">
        <i class="fas fa-${icons[type] || 'info-circle'} me-2"></i>${message}
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="this.closest('.toast').remove()"></button>
    </div>`;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
}

function createToastContainer() {
  const div = document.createElement('div');
  div.id = 'toast-container';
  div.style.cssText = 'position:fixed;top:75px;right:20px;z-index:9999;min-width:300px';
  document.body.appendChild(div);
  return div;
}

// ─── SCROLL TO TOP ─────────────────────────────
const scrollBtn = document.getElementById('scrollTop');
if (scrollBtn) {
  window.addEventListener('scroll', () => {
    scrollBtn.style.display = window.scrollY > 300 ? 'flex' : 'none';
  });
  scrollBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

// ─── NAVBAR SHRINK ON SCROLL ───────────────────
const navbar = document.querySelector('.navbar');
if (navbar) {
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
  });
}

// ─── TOGGLE FAVORI ────────────────────────────
function toggleFavori(type, id, btn) {
  if (!btn) return;
  fetch('/api/favori/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({ type, id })
  })
  .then(r => r.json())
  .then(data => {
    const isAdded = data.status === 'added';
    btn.classList.toggle('active', isAdded);
    const icon = btn.querySelector('i');
    if (icon) icon.className = `${isAdded ? 'fas' : 'far'} fa-heart`;
    showToast(isAdded ? 'Ajouté aux favoris !' : 'Retiré des favoris.', isAdded ? 'success' : 'info');
  })
  .catch(() => showToast('Erreur. Veuillez vous connecter.', 'danger'));
}

// ─── MARQUER NOTIFICATIONS LUES ───────────────
function marquerLu() {
  fetch('/api/notifications/lire/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken') }
  })
  .then(() => {
    document.querySelectorAll('.notif-badge').forEach(b => b.remove());
  });
}

// ─── CALCUL PRIX RÉSERVATION ───────────────────
function calculerPrix() {
  const d1El = document.getElementById('id_date_debut');
  const d2El = document.getElementById('id_date_fin');
  const hebEl = document.getElementById('id_hebergement');
  const guideEl = document.getElementById('id_guide');
  const nbEl = document.getElementById('id_nb_personnes');
  const totalEl = document.getElementById('prix-total');

  if (!d1El || !d2El || !totalEl) return;

  const d1 = new Date(d1El.value);
  const d2 = new Date(d2El.value);
  if (!d1El.value || !d2El.value || d2 <= d1) {
    totalEl.textContent = '–';
    return;
  }

  const nuits = Math.ceil((d2 - d1) / (1000 * 60 * 60 * 24));
  const nb = parseInt(nbEl?.value || 1);
  let total = 0;

  if (hebEl) {
    const opt = hebEl.options[hebEl.selectedIndex];
    const prix = parseFloat(opt?.dataset.prix || 0);
    total += prix * nuits;
  }

  if (guideEl) {
    const opt = guideEl.options[guideEl.selectedIndex];
    const prix = parseFloat(opt?.dataset.prix || 0);
    total += prix * nuits * nb;
  }

  totalEl.textContent = total > 0 ? total.toFixed(2) + ' MRU' : '–';

  // Afficher le détail
  const detailEl = document.getElementById('prix-detail');
  if (detailEl && nuits > 0) {
    detailEl.textContent = `${nuits} nuit${nuits > 1 ? 's' : ''} · ${nb} personne${nb > 1 ? 's' : ''}`;
  }
}

// ─── COMPARAISON HÉBERGEMENTS ──────────────────
const compareSet = new Set(JSON.parse(localStorage.getItem('compare_ids') || '[]'));

function toggleCompare(id, btn) {
  if (compareSet.has(id)) {
    compareSet.delete(id);
    btn.textContent = '+ Comparer';
    btn.classList.remove('btn-ocean');
    btn.classList.add('btn-outline-secondary');
    showToast('Retiré de la comparaison.', 'info');
  } else {
    if (compareSet.size >= 3) {
      showToast('Vous pouvez comparer 3 hébergements maximum.', 'warning');
      return;
    }
    compareSet.add(id);
    btn.textContent = '✓ Comparaison';
    btn.classList.remove('btn-outline-secondary');
    btn.classList.add('btn-ocean');
    showToast('Ajouté à la comparaison !', 'success');
  }
  localStorage.setItem('compare_ids', JSON.stringify([...compareSet]));
  updateCompareBar();
}

function updateCompareBar() {
  let bar = document.getElementById('compare-bar');
  if (compareSet.size === 0) {
    if (bar) bar.remove();
    return;
  }
  if (!bar) {
    bar = document.createElement('div');
    bar.id = 'compare-bar';
    bar.style.cssText = `
      position: fixed; bottom: 0; left: 0; right: 0; z-index: 1050;
      background: var(--nuit); color: #fff;
      padding: .85rem 1.5rem;
      display: flex; align-items: center; justify-content: space-between;
      box-shadow: 0 -4px 20px rgba(0,0,0,.3);
      animation: fadeInUp .3s ease;
    `;
    document.body.appendChild(bar);
  }
  bar.innerHTML = `
    <span><i class="fas fa-balance-scale me-2" style="color:var(--sable)"></i>
      <strong>${compareSet.size}</strong> hébergement${compareSet.size > 1 ? 's' : ''} sélectionné${compareSet.size > 1 ? 's' : ''}
    </span>
    <div class="d-flex gap-2">
      ${compareSet.size >= 2 ? `<a href="/hebergements/comparer/?${[...compareSet].map(id => 'ids=' + id).join('&')}" class="btn btn-mauritanie btn-sm"><i class="fas fa-balance-scale me-1"></i>Comparer</a>` : '<span class="text-muted small">Sélectionnez au moins 2</span>'}
      <button onclick="clearCompare()" class="btn btn-outline-light btn-sm">Vider</button>
    </div>`;
}

function clearCompare() {
  compareSet.clear();
  localStorage.removeItem('compare_ids');
  updateCompareBar();
  document.querySelectorAll('.btn-compare').forEach(b => {
    b.textContent = '+ Comparer';
    b.classList.remove('btn-ocean');
    b.classList.add('btn-outline-secondary');
  });
}

// ─── GALERIE IMAGES ───────────────────────────
function openLightbox(src, alt) {
  const lb = document.createElement('div');
  lb.style.cssText = `
    position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.92);
    display:flex;align-items:center;justify-content:center;cursor:pointer;
    animation:fadeInUp .2s ease;
  `;
  lb.innerHTML = `
    <div style="position:relative;max-width:90vw;max-height:90vh">
      <img src="${src}" alt="${alt}" style="max-width:100%;max-height:90vh;border-radius:12px;box-shadow:0 10px 60px rgba(0,0,0,.5)">
      <button onclick="this.closest('[style]').remove()" style="position:absolute;top:-15px;right:-15px;background:var(--desert);color:#fff;border:none;border-radius:50%;width:36px;height:36px;font-size:1.1rem;cursor:pointer;display:flex;align-items:center;justify-content:center">
        <i class="fas fa-times"></i>
      </button>
    </div>`;
  lb.addEventListener('click', e => { if (e.target === lb) lb.remove(); });
  document.body.appendChild(lb);
}

// ─── CONFIRMATION ACTIONS DANGEREUSES ─────────
document.querySelectorAll('[data-confirm]').forEach(el => {
  el.addEventListener('click', e => {
    if (!confirm(el.dataset.confirm)) e.preventDefault();
  });
});

// ─── INIT AU CHARGEMENT ────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Activer calcul prix dynamique
  ['id_date_debut', 'id_date_fin', 'id_hebergement', 'id_guide', 'id_nb_personnes'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', calculerPrix);
  });

  // Restaurer état comparaison
  updateCompareBar();

  // Animations au scroll
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in-up');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.card-tourisme, .stat-card').forEach(el => observer.observe(el));

  // Activer tooltips Bootstrap
  document.querySelectorAll('[title]').forEach(el => {
    new bootstrap.Tooltip(el, { trigger: 'hover' });
  });

  // Auto-dismiss alerts après 5s
  document.querySelectorAll('.alert.alert-dismissible').forEach(alert => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });
});
