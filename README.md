# Arena Web — The Elder Scrolls: Arena (1994) en el navegador

Porte de **The Elder Scrolls: Arena** (1994) a WebAssembly usando [js-dos v8](https://js-dos.com/) (DOSBox compilado a WASM). Sin plugins, corre en cualquier navegador moderno.

## Juego jugable

**https://tes-arena-1994.vercel.app**

> Nota: el proyecto usa *Deployment Protection* de Vercel, así que puede pedirte iniciar sesión en Vercel antes de mostrar el juego.

Porteado por [Franco Castillo (FrancoCastillo1)](https://github.com/FrancoCastillo1).

## Aclaración sobre los assets (importante)

**No se incluye la carpeta `bundle/` ni los archivos `.jsdos`** en este repositorio.

Motivos:

- **Derechos de autor:** Arena es un juego de Bethesda Softworks. La música, gráficos, textos y datos del juego (`GLOBAL.BSA`, los `.MIF`, `ACD.EXE`, videos `.FLC`, etc.) son propiedad de sus titulares y no deben redistribuirse públicamente.
- **Almacenamiento:** esos archivos pesan decenas de MB y no aportan al código del porte.

Este repo contiene **solo el código y la configuración del porte**. Para jugar, obtén tu propia copia del juego (por ejemplo desde [GOG.com](https://www.gog.com)) y construye el bundle localmente (ver más abajo).

## Cómo funciona

1. `index.html` carga el emulador **js-dos** desde su CDN.
2. Descarga el bundle `.jsdos` (un ZIP con el juego + `dosbox.conf`).
3. Arranca DOSBox/WASM en un `<canvas>` y ejecuta `ACD.EXE` (el launcher de la versión CD de Arena).

### Rendimiento (DOSBox/WASM)

- El build WASM de DOSBox **no tiene core dinámico (JIT)**: solo intérprete. `core=dynamic` no aplica en navegador.
- Config usada (equilibrada, estable y sin ruido de audio):
  - `cycles=fixed 30000`
  - `scaler=none`, `aspect=false`, `frameskip=1`
  - `machine=svga_s3`, `memsize=32`, `rate=44100`
- El player usa `offscreenCanvas: true` (render fuera del hilo principal) e `imageRendering: "pixelated"`.

### Caché

El bundle se sirve con `Cache-Control: immutable` (ver `deploy/vercel.json`) y el nombre incluye versión (`arena-v4.jsdos`), así que solo se descarga la primera vez. Para forzar una actualización, cambia la versión en el nombre del archivo.

## Estructura

```
arena-web/
├── index.html          # Player local (versión simple)
├── build_bundle.py     # Genera el bundle .jsdos desde bundle/
├── serve.py            # Servidor local sin caché (puerto 8000)
├── test_serve.py       # Tests del servidor
├── jugar.ps1           # Arranque local en Windows
├── bundle/             # TU copia del juego (no versionada) + dosbox.conf
└── deploy/             # Artefacto desplegado en Vercel
    ├── index.html      # Player con pantalla de carga + progreso + crédito
    ├── vercel.json     # Headers de caché
    └── .vercel/        # Link del proyecto Vercel (no versionado)
```

## Uso local

1. Copia los archivos de tu Arena a `arena-web/bundle/` (excluye instaladores, el PDF del manual, `SPEECH`, `cloud_saves` y el DOSBOX embebido de GOG si lo hay).
2. Ajusta `arena-web/bundle/dosbox.conf` si hace falta.
3. Construye el bundle:

   ```powershell
   python build_bundle.py
   ```

4. Sirve en local y abre el navegador:

   ```powershell
   python serve.py
   # → http://localhost:8000
   ```

> `build_bundle.py` espera la estructura `.jsdos/` dentro del ZIP (directorio + `.jsdos/dosbox.conf`). PowerShell 5.1 falla con extensiones `.jsdos`; usa el script de Python.

## Despliegue en Vercel

El directorio desplegado es `deploy/`. Copia ahí el bundle recién generado y despliega:

```powershell
cd deploy
& "C:\Program Files\nodejs\npx.cmd" --yes vercel@latest deploy --prod --yes
```

> `npx` puede estar bloqueado por la execution policy de PowerShell; usar la ruta absoluta a `npx.cmd` como arriba.

### Notas para el despliegue

- Si cambias la config de DOSBox, vuelve a ejecutar `build_bundle.py` y **cambia la versión del nombre** del `.jsdos` (por ejemplo a `arena-v5.jsdos`) en `deploy/index.html` y `deploy/vercel.json`.
- No subas tokens ni credenciales a este repo.

## Créditos

- Juego original: **The Elder Scrolls: Arena** (1994), Bethesda Softworks. © Bethesda.
- Emulación: [js-dos](https://js-dos.com/) / DOSBox.
- Porte web: [Franco Castillo (FrancoCastillo1)](https://github.com/FrancoCastillo1).

## Licencia del código

El código de porte en este repo se ofrece "tal cual", sin garantías. Los assets del juego no están incluidos y permanecen bajo la licencia de sus titulares.
