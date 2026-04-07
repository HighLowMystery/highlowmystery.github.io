// Affiliate Base Theme — Main JS
// Minimal, zero-dependency

// Mobile nav toggle (backup for browsers without onclick support)
document.addEventListener('DOMContentLoaded', function() {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => nav.classList.toggle('open'));
    // Close nav when a link is clicked
    nav.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => nav.classList.remove('open'));
    });
  }

  // Smooth scroll for TOC links
  document.querySelectorAll('.toc-box a').forEach(link => {
    link.addEventListener('click', e => {
      const href = link.getAttribute('href');
      if (href && href.startsWith('#')) {
        e.preventDefault();
        const target = document.getElementById(href.slice(1));
        if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Track outbound affiliate clicks (no external service needed)
  document.querySelectorAll('a[rel*="sponsored"]').forEach(link => {
    link.addEventListener('click', function() {
      const name = this.closest('.product-card')?.querySelector('.product-name')?.textContent || 'unknown';
      console.log('[Affiliate Click]', name, this.href);
      // Replace with your analytics event if needed
    });
  });
});
