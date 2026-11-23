# Blue Light · Versión web

Exportación web de **Blue Light** hecha con Godot 4.7 (`index.html`, `index.js`, `index.wasm`, `index.pck` y demás archivos de la exportación). Se despliega en Netlify: [webbluelight.netlify.app](https://webbluelight.netlify.app/).

## Parte de un repositorio mayor

Este repo es un submódulo de [BlueLight_Yarbis](https://github.com/AndresLizcano-Gjthub/BlueLight_Yarbis), que contiene el código fuente del juego. Ahí aparece como la carpeta `build-web`.

El archivo `.gdignore` hace que Godot ignore esta carpeta cuando se abre el proyecto principal. No lo borres.

## Cómo actualizarla

Estos archivos se generan al exportar, así que no se editan a mano.

1. En Godot, exporta el proyecto para Web sobre esta carpeta y haz push a `main` de este repo.
2. En `BlueLight_Yarbis`, actualiza el puntero del submódulo: `git add build-web`, `git commit` y `git push`.
