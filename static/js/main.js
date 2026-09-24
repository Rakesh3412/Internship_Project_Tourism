/**
 * TourVista - Main Interactive JavaScript
 */

document.addEventListener('DOMContentLoaded', () => {
  initWishlistToggles();
  initGlobalLiveSearch();
  initGallerySwitcher();
});

/* ==========================================================================
   1. AJAX Wishlist / Bucket List Toggle
   ========================================================================== */
function initWishlistToggles() {
  document.querySelectorAll('.btn-wishlist').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      e.stopPropagation();

      const placeId = btn.getAttribute('data-place-id');
      if (!placeId) return;

      try {
        const response = await fetch(`/wishlist/toggle/${placeId}/`, {
          method: 'GET',
          headers: {
            'X-Requested-With': 'XMLHttpRequest'
          }
        });

        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();

        if (data.status === 'success') {
          // Toggle UI state
          if (data.in_wishlist) {
            btn.classList.add('active');
            btn.innerHTML = '<i class="fas fa-heart"></i>';
          } else {
            btn.classList.remove('active');
            btn.innerHTML = '<i class="far fa-heart"></i>';
          }

          // Update header wishlist badge count
          const badge = document.getElementById('wishlistCountBadge');
          if (badge) {
            badge.textContent = data.count;
            badge.style.display = data.count > 0 ? 'inline-block' : 'none';
          }

          showToast(data.message, data.in_wishlist ? 'success' : 'info');

          // If on wishlist page and removed, remove card element
          if (!data.in_wishlist && window.location.pathname.includes('/wishlist/')) {
            const cardCol = btn.closest('.wishlist-card-col');
            if (cardCol) {
              cardCol.style.transition = 'all 0.3s ease';
              cardCol.style.opacity = '0';
              cardCol.style.transform = 'scale(0.9)';
              setTimeout(() => {
                cardCol.remove();
                if (document.querySelectorAll('.wishlist-card-col').length === 0) {
                  location.reload();
                }
              }, 300);
            }
          }
        }
      } catch (err) {
        console.error('Error toggling wishlist:', err);
        showToast('Could not update wishlist. Please try again.', 'error');
      }
    });
  });
}

/* ==========================================================================
   2. Global Live Search with Debounce & Autocomplete Modal
   ========================================================================== */
function initGlobalLiveSearch() {
  const searchInput = document.getElementById('globalLiveSearchInput');
  const resultsContainer = document.getElementById('globalSearchResults');
  if (!searchInput || !resultsContainer) return;

  let debounceTimer;

  searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    const query = searchInput.value.trim();

    if (query.length < 2) {
      resultsContainer.innerHTML = '<div class="text-center py-4 text-muted"><i class="fas fa-search fa-2x mb-2 text-light"></i><p class="mb-0">Type at least 2 characters to search states and places...</p></div>';
      return;
    }

    resultsContainer.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary spinner-border-sm" role="status"></div><span class="ms-2 text-muted">Searching destinations...</span></div>';

    debounceTimer = setTimeout(async () => {
      try {
        const res = await fetch(`/api/search/?q=${encodeURIComponent(query)}`);
        const data = await res.json();

        if (!data.results || data.results.length === 0) {
          resultsContainer.innerHTML = `<div class="text-center py-4 text-muted"><p class="mb-1">No destinations found matching "<b>${escapeHtml(query)}</b>"</p><small class="text-light">Try searching for Kerala, Jaipur, Manali, beaches, or forts</small></div>`;
          return;
        }

        let html = '<div class="list-group list-group-flush">';
        data.results.forEach(item => {
          const typeBadge = item.type === 'State' 
            ? '<span class="badge bg-primary-subtle text-primary">State</span>' 
            : `<span class="badge bg-amber-subtle text-warning"><i class="fas fa-star text-warning me-1"></i>${item.rating || '4.8'}</span>`;

          html += `
            <a href="${item.url}" class="list-group-item list-group-item-action d-flex align-items-center gap-3 py-2 px-3 border-0 rounded-3 mb-1 search-item">
              <img src="${item.image}" alt="${escapeHtml(item.title)}" style="width: 48px; height: 48px; object-fit: cover; border-radius: 8px;">
              <div class="flex-grow-1">
                <div class="d-flex align-items-center justify-content-between">
                  <h6 class="mb-0 fw-bold">${escapeHtml(item.title)}</h6>
                  ${typeBadge}
                </div>
                <small class="text-muted">${escapeHtml(item.subtitle)}</small>
              </div>
            </a>
          `;
        });
        html += '</div>';

        resultsContainer.innerHTML = html;
      } catch (e) {
        console.error('Search error:', e);
        resultsContainer.innerHTML = '<div class="text-danger py-3 text-center">Failed to fetch search results.</div>';
      }
    }, 250);
  });
}

/* ==========================================================================
   3. Leaflet Interactive Maps Initializer
   ========================================================================== */
function initTourismMap(containerId, markers, defaultCenter = [20.5937, 78.9629], defaultZoom = 5) {
  const mapElement = document.getElementById(containerId);
  if (!mapElement || typeof L === 'undefined') return;

  // If map already initialized on this element, remove it
  if (mapElement._leaflet_id) {
    return;
  }

  let center = defaultCenter;
  let zoom = defaultZoom;

  if (markers && markers.length > 0) {
    center = [markers[0].lat, markers[0].lng];
    if (markers.length === 1) {
      zoom = 13;
    } else {
      zoom = 8;
    }
  }

  const map = L.map(containerId, {
    scrollWheelZoom: false
  }).setView(center, zoom);

  // Add OpenStreetMap tiles with attribution
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  if (markers && markers.length > 0) {
    const latLngBounds = [];

    markers.forEach(m => {
      if (!m.lat || !m.lng) return;

      const marker = L.marker([m.lat, m.lng]).addTo(map);
      latLngBounds.push([m.lat, m.lng]);

      const popupContent = `
        <div class="map-popup-card">
          <img src="${m.image}" alt="${escapeHtml(m.name)}" />
          <h6 class="map-popup-title">${escapeHtml(m.name)}</h6>
          <p class="text-muted small mb-1"><i class="fas fa-map-pin text-primary me-1"></i>${escapeHtml(m.city)}</p>
          <div class="d-flex justify-content-between align-items-center mt-2">
            <span class="badge bg-warning text-dark"><i class="fas fa-star me-1"></i>${m.rating || '4.8'}</span>
            <a href="${m.url}" class="btn btn-sm btn-primary py-0 px-2" style="font-size: 11px;">Explore</a>
          </div>
        </div>
      `;

      marker.bindPopup(popupContent);
    });

    if (markers.length > 1) {
      map.fitBounds(latLngBounds, { padding: [30, 30] });
    }
  }
}

/* ==========================================================================
   4. Gallery Image Switcher
   ========================================================================== */
function initGallerySwitcher() {
  const mainImage = document.getElementById('placeMainImage');
  const thumbs = document.querySelectorAll('.gallery-thumb-btn');

  if (!mainImage || thumbs.length === 0) return;

  thumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      thumbs.forEach(t => t.classList.remove('border-primary', 'shadow'));
      thumb.classList.add('border-primary', 'shadow');

      const fullSrc = thumb.getAttribute('data-img-src');
      if (fullSrc) {
        mainImage.style.opacity = '0.4';
        setTimeout(() => {
          mainImage.src = fullSrc;
          mainImage.style.opacity = '1';
        }, 150);
      }
    });
  });
}

/* ==========================================================================
   5. Floating Toast Notification Utility
   ========================================================================== */
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const icons = {
    success: 'fa-check-circle text-success',
    error: 'fa-exclamation-circle text-danger',
    info: 'fa-info-circle text-primary'
  };

  const toastEl = document.createElement('div');
  toastEl.className = 'toast align-items-center text-bg-white border shadow-lg show mb-2';
  toastEl.setAttribute('role', 'alert');
  toastEl.setAttribute('aria-live', 'assertive');
  toastEl.setAttribute('aria-atomic', 'true');

  toastEl.innerHTML = `
    <div class="d-flex">
      <div class="toast-body d-flex align-items-center gap-2">
        <i class="fas ${icons[type] || icons.info} fa-lg"></i>
        <span>${escapeHtml(message)}</span>
      </div>
      <button type="button" class="btn-close me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  `;

  container.appendChild(toastEl);

  setTimeout(() => {
    toastEl.classList.remove('show');
    setTimeout(() => toastEl.remove(), 300);
  }, 3500);
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
