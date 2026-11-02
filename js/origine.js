/* Origine de la visite (ex. ?utm_source=verification-incendie.fr) : recopiée sur
   les liens vers les autres pages du site et vers l'app, pour qu'elle suive le
   visiteur jusqu'à l'inscription. Ni cookie ni stockage dans le navigateur. */
(function () {
  var params = new URLSearchParams(window.location.search);
  var keys = ['utm_source', 'utm_medium', 'utm_campaign'].filter(function (k) { return params.get(k); });
  if (!keys.length) return;

  function withSource(href) {
    var url;
    try { url = new URL(href, window.location.href); } catch (e) { return href; }
    var host = url.hostname.replace(/^www\./, '');
    if (host !== 'firovia.fr' && host !== 'app.firovia.fr' && url.hostname !== window.location.hostname) return href;
    keys.forEach(function (k) { if (!url.searchParams.has(k)) url.searchParams.set(k, params.get(k)); });
    return url.origin === window.location.origin ? url.pathname + url.search + url.hash : url.toString();
  }
  window.firoviaWithSource = withSource;

  function decorate() {
    document.querySelectorAll('a[href]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (!href || href.charAt(0) === '#' || /^(mailto|tel|javascript):/i.test(href)) return;
      a.setAttribute('href', withSource(href));
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', decorate);
  else decorate();
})();
