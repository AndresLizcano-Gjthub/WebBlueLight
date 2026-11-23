"""Parte index.pck en trozos de <95 MB (límite de GitHub: 100 MB por archivo)
y mete en index.html un pequeño script que, cuando el motor pide index.pck,
descarga los trozos en orden y se los entrega como si fuera un solo archivo."""
import os, sys, json
d = sys.argv[1]
pck = os.path.join(d, "index.pck")
TROZO = 95_000_000
datos_total = os.path.getsize(pck)
partes = []
with open(pck, "rb") as f:
    i = 0
    while True:
        b = f.read(TROZO)
        if not b:
            break
        nombre = "index.pck.%d" % i
        with open(os.path.join(d, nombre), "wb") as o:
            o.write(b)
        partes.append(nombre)
        i += 1
os.remove(pck)
shim = """<script>
// index.pck va partido en trozos (GitHub no acepta archivos de más de 100 MB).
(function () {
	const PARTES = %s;
	const TOTAL = %d;
	const fetchOriginal = window.fetch.bind(window);
	window.fetch = function (recurso, opciones) {
		const url = typeof recurso === 'string' ? recurso : (recurso && recurso.url) || '';
		if (!/(^|\\/)index\\.pck(\\?|$)/.test(url)) {
			return fetchOriginal(recurso, opciones);
		}
		let n = 0;
		let lector = null;
		const flujo = new ReadableStream({
			async pull(control) {
				while (true) {
					if (!lector) {
						if (n >= PARTES.length) { control.close(); return; }
						const r = await fetchOriginal(PARTES[n++], { cache: 'no-cache' });
						if (!r.ok) { control.error(new Error('No se pudo bajar ' + PARTES[n - 1])); return; }
						lector = r.body.getReader();
					}
					const { done, value } = await lector.read();
					if (done) { lector = null; continue; }
					control.enqueue(value);
					return;
				}
			}
		});
		return Promise.resolve(new Response(flujo, {
			status: 200,
			headers: { 'Content-Type': 'application/octet-stream', 'Content-Length': String(TOTAL) }
		}));
	};
})();
</script>
""" % (json.dumps(partes), datos_total)
h = os.path.join(d, "index.html")
t = open(h, encoding="utf-8").read()
marca = '<script src="index.js"></script>'
assert marca in t and "PARTES" not in t
t = t.replace(marca, shim + "\t\t" + marca, 1)
open(h, "w", encoding="utf-8").write(t)
print(partes, datos_total)
