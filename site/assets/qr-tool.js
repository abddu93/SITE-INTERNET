(function () {
  var form = document.getElementById('qr-form');
  if (!form || typeof qrcode !== 'function') return;
  var url = document.getElementById('qr-url');
  var label = document.getElementById('qr-label');
  var out = document.getElementById('qr-out');
  var caption = document.getElementById('qr-caption');
  var dlSvg = document.getElementById('qr-svg');
  var dlPng = document.getElementById('qr-png');
  var error = document.getElementById('qr-error');
  var svgText = '';

  function valid(v) { return /^https?:\/\/[^\s.]+\.[^\s]+$/i.test(v); }

  function render() {
    var v = url.value.trim();
    var ok = valid(v);
    error.hidden = ok || v === '';
    dlSvg.setAttribute('aria-disabled', String(!ok));
    dlPng.setAttribute('aria-disabled', String(!ok));
    if (!ok) {
      out.innerHTML = '<p class="muted">Votre QR code apparaîtra ici.</p>';
      caption.textContent = '';
      svgText = '';
      return;
    }
    var q = qrcode(0, 'M');
    q.addData(v);
    q.make();
    svgText = q.createSvgTag({ cellSize: 8, margin: 4, scalable: true, alt: 'QR code vers ' + v });
    out.innerHTML = svgText;
    caption.textContent = label.value.trim();
  }

  function download(name, href) {
    var a = document.createElement('a');
    a.href = href;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  dlSvg.addEventListener('click', function (e) {
    e.preventDefault();
    if (!svgText) return;
    download('qr-code.svg', 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgText));
  });

  dlPng.addEventListener('click', function (e) {
    e.preventDefault();
    if (!svgText) return;
    var img = new Image();
    img.onload = function () {
      var size = 1200;
      var c = document.createElement('canvas');
      c.width = size; c.height = size;
      var ctx = c.getContext('2d');
      ctx.fillStyle = '#fff';
      ctx.fillRect(0, 0, size, size);
      ctx.drawImage(img, 0, 0, size, size);
      download('qr-code.png', c.toDataURL('image/png'));
    };
    img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgText);
  });

  form.addEventListener('input', render);
  form.addEventListener('submit', function (e) { e.preventDefault(); render(); });
  render();
})();
