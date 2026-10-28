(function () {
  var FRAIS_DIRECT = 0.06; // ~2 % de frais de paiement en ligne + ~4 % de remise de bienvenue
  var form = document.getElementById('calc');
  if (!form) return;

  var ventes = document.getElementById('ventes');
  var taux = document.getElementById('taux');
  var tva = document.getElementById('tva');
  var part = document.getElementById('part');
  var partLabel = document.getElementById('part-label');
  var chips = form.querySelectorAll('.chip');

  var out = {
    mois: document.getElementById('r-mois'),
    an: document.getElementById('r-an'),
    effectif: document.getElementById('r-effectif'),
    bascule: document.getElementById('r-bascule'),
    garde: document.getElementById('r-garde'),
    gardeAn: document.getElementById('r-garde-an'),
    alerte: document.getElementById('r-alerte')
  };

  var euros = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
  var pct = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 1 });

  function num(input, fallback) {
    var v = parseFloat(String(input.value).replace(',', '.'));
    return isFinite(v) && v >= 0 ? v : fallback;
  }

  function calc() {
    var v = num(ventes, 0);
    var t = Math.min(num(taux, 0), 100) / 100;
    var tEff = tva.checked ? t * 1.2 : t;
    var p = num(part, 0) / 100;

    var mois = v * tEff;
    var basculees = v * p;
    var garde = basculees * (tEff - FRAIS_DIRECT);

    partLabel.textContent = Math.round(p * 100) + ' %';
    out.mois.textContent = euros.format(mois);
    out.an.textContent = euros.format(mois * 12);
    out.effectif.textContent = pct.format(tEff * 100) + ' %';
    out.bascule.textContent = euros.format(basculees);
    out.garde.textContent = euros.format(Math.max(garde, 0));
    out.gardeAn.textContent = euros.format(Math.max(garde, 0) * 12);
    out.alerte.hidden = garde > 0 || basculees === 0;

    chips.forEach(function (c) {
      c.setAttribute('aria-pressed', String(Number(c.dataset.taux) === Math.round(t * 100)));
    });
  }

  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      taux.value = c.dataset.taux;
      calc();
    });
  });
  form.addEventListener('input', calc);
  form.addEventListener('submit', function (e) { e.preventDefault(); calc(); });
  calc();
})();
