import zipfile, os, sys

VERSION = "v4"          # Cambia esto para invalidar la cache del navegador
OUT_NAME = "arena-%s.jsdos" % VERSION

base = os.path.dirname(os.path.abspath(__file__))
bundle_dir = os.path.join(base, "bundle")
conf_path = os.path.join(base, "dosbox.conf")
out = os.path.join(base, OUT_NAME)

# Configs de GOG que no deben entrar al bundle
skip = {"dosbox.conf", "jsdos.json", "dosbox_arena.conf", "dosbox_arena_single.conf"}

# --- Validaciones antes de empaquetar ---
if not os.path.isfile(conf_path):
    sys.exit("Falta dosbox.conf en la raíz del proyecto (junto a build_bundle.py).")

game_files = []
if os.path.isdir(bundle_dir):
    game_files = [n for n in sorted(os.listdir(bundle_dir))
                  if n not in skip and os.path.isfile(os.path.join(bundle_dir, n))]

if not game_files:
    sys.exit(
        "No hay juego en bundle/.\n"
        "Copia tu propia Arena (por ejemplo desde GOG) a la carpeta bundle/\n"
        "y vuelve a ejecutar: python build_bundle.py"
    )

if "ACD.EXE" not in game_files:
    sys.exit(
        "No encontré ACD.EXE en bundle/.\n"
        "Parece que ahí no está la versión CD de Arena (1.07)."
    )

# --- Empaquetado ---
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    # 1) Entrada de directorio explícita .jsdos/ (requerida por libzip de js-dos)
    dirinfo = zipfile.ZipInfo(".jsdos/")
    dirinfo.external_attr = (0o40755 << 16) | 0x10  # directorio
    z.writestr(dirinfo, "")

    # 2) Config dentro de .jsdos/ (desde la raíz, no desde bundle/)
    z.write(conf_path, ".jsdos/dosbox.conf")

    # 3) Override corto en la raíz (como el bundle oficial)
    z.writestr("dosbox.conf", "[cpu]\r\ncycles=fixed 30000\r\n")

    # 4) Juego en la raíz
    for name in game_files:
        z.write(os.path.join(bundle_dir, name), name)

# --- Verificación ---
with zipfile.ZipFile(out) as z:
    infos = z.infolist()
    names = [i.filename for i in infos]
    checks = {
        "directorio .jsdos/ (is_dir)": any(i.filename == ".jsdos/" and i.is_dir() for i in infos),
        ".jsdos/dosbox.conf": ".jsdos/dosbox.conf" in names,
        "dosbox.conf raiz": "dosbox.conf" in names,
        "ACD.EXE": "ACD.EXE" in names,
        "GLOBAL.BSA": "GLOBAL.BSA" in names,
        "sin backslashes": not any("\\" in n for n in names),
        "sin jsdos.json": not any(n.endswith("jsdos.json") for n in names),
    }
    ok = True
    for k, v in checks.items():
        print(("OK  " if v else "FAIL") + " " + k)
        ok = ok and v
    print()
    print("Primeras 6 entradas (orden del zip):")
    for i in infos[:6]:
        print("  %r dir=%s size=%d" % (i.filename, i.is_dir(), i.file_size))

print()
print("salida: %s  (%.1f MB)" % (OUT_NAME, os.path.getsize(out) / 1024 / 1024))
sys.exit(0 if ok else 1)
