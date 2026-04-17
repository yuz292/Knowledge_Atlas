/* ────────────────────────────────────────────────────────────────
   ka_user_type.js — shared access-control companion for K-ATLAS
   Include on every page:   <script src="ka_user_type.js" defer></script>

   Model
   -----
   Public user types (anyone, no login):
     visitor, researcher, practitioner, contributor
   Gated user types (login required):
     160-student, instructor

   Admin override
   --------------
   When ka.admin === 'yes' and ka.impersonating === 'true', the admin is
   silently viewing the site as another user type. A persistent amber banner
   at the top of every page confirms the impersonation and offers one-click
   return-to-admin or stop-impersonating.

   Per-element gating
   ------------------
   Mark any element that only enrolled students should see:
     <div data-ka-requires="160-student"> … </div>
   The element is hidden from unauthenticated visitors but remains visible
   for admins impersonating 160 Student (or for the student themselves).

   Replace storage (sessionStorage) with a server-backed session cookie in
   production. See ka_admin.html → ADMIN_API for the corresponding seam.
   ──────────────────────────────────────────────────────────────── */

(function () {
  'use strict';

  var PUBLIC_TYPES = ['visitor', 'researcher', 'practitioner', 'contributor'];
  var GATED_TYPES  = ['160-student', 'instructor'];

  var SS = window.sessionStorage;
  function g(k) { try { return SS.getItem(k); } catch (e) { return null; } }
  function s(k, v) { try { SS.setItem(k, v); } catch (e) {} }
  function rm(k) { try { SS.removeItem(k); } catch (e) {} }

  var KA = window.KA = window.KA || {};

  KA.userType = {
    /** Which user type is the viewer currently acting as? */
    get: function () { return g('ka.userType') || 'visitor'; },

    /** Set the viewer's user type. Pass {impersonate:true} for admin override. */
    set: function (type, opts) {
      opts = opts || {};
      s('ka.userType', type);
      if (opts.impersonate) s('ka.impersonating', 'true');
      else rm('ka.impersonating');
      if (opts.reload !== false) location.reload();
    },

    isPublic: function (t) { return PUBLIC_TYPES.indexOf(t) >= 0; },
    isGated:  function (t) { return GATED_TYPES.indexOf(t)  >= 0; },
    isAdmin:  function ()  { return g('ka.admin') === 'yes'; },
    isImpersonating: function () { return g('ka.impersonating') === 'true'; },

    /**
     * May the current viewer see content marked for `type`?
     *  - public types: always yes
     *  - gated types: yes if the viewer authenticated for that type,
     *                 or if an admin is impersonating that type.
     */
    canSee: function (type) {
      if (!type || PUBLIC_TYPES.indexOf(type) >= 0) return true;
      if (KA.userType.isAdmin()) return true;
      if (type === '160-student') return g('ka.160.authed') === 'yes';
      if (type === 'instructor')  return g('ka.admin') === 'yes';
      return false;
    },

    stopImpersonating: function () {
      rm('ka.impersonating');
      s('ka.userType', 'instructor');
      location.reload();
    }
  };

  /* ─── Impersonation banner ─── */
  function mountBanner() {
    if (!KA.userType.isAdmin() || !KA.userType.isImpersonating()) return;
    var ut = KA.userType.get();
    var bar = document.createElement('div');
    bar.id = 'ka-imp-banner';
    bar.setAttribute('role', 'status');
    bar.style.cssText =
      'position:fixed;top:0;left:0;right:0;z-index:9999;' +
      'background:#E8872A;color:#fff;padding:6px 16px;text-align:center;' +
      'font:600 0.82rem -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;' +
      'box-shadow:0 2px 6px rgba(0,0,0,0.2);';
    bar.innerHTML =
      'Viewing as <b>' + esc(ut) + '</b> &middot; ' +
      '<a href="160sp/ka_admin.html" style="color:#fff;text-decoration:underline;">Return to admin</a> &middot; ' +
      '<a href="#" id="ka-imp-stop" style="color:#fff;text-decoration:underline;">Stop impersonating</a>';
    document.body.insertBefore(bar, document.body.firstChild);
    document.body.style.paddingTop =
      ((parseInt(getComputedStyle(document.body).paddingTop, 10) || 0) + 32) + 'px';
    var stop = document.getElementById('ka-imp-stop');
    if (stop) stop.addEventListener('click', function (e) {
      e.preventDefault();
      KA.userType.stopImpersonating();
    });
  }

  /* ─── Per-element gating ─── */
  function applyElementGates() {
    var els = document.querySelectorAll('[data-ka-requires]');
    for (var i = 0; i < els.length; i++) {
      var need = els[i].getAttribute('data-ka-requires');
      if (!KA.userType.canSee(need)) {
        els[i].style.display = 'none';
        els[i].setAttribute('data-ka-gated', 'hidden');
      } else {
        els[i].removeAttribute('data-ka-gated');
      }
    }
  }

  /* ─── Helpers ─── */
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' })[c];
    });
  }

  /* ─── Boot (after DOM) ─── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      mountBanner();
      applyElementGates();
    });
  } else {
    mountBanner();
    applyElementGates();
  }
})();
