import zipfile, os, sys

base = os.path.dirname(os.path.abspath(__file__))
bundle_dir = os.path.join(base, "bundle")
out = os.path.join(base, "arena-v4.jsdos")

skip = {"dosbox.conf", "jsdos.json", "dosbox_arena.conf", "dosbox_arena_single.conf"}

with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    # 1) Entrada de directorio explícita .jsdos/ (requerida por libzip de js-dos)
    dirinfo = zipfile.ZipInfo(".jsdos/")
    dirinfo.external_attr = (0o40755 << 16) | 0x10  # directorio
    z.writestr(dirinfo, "")

    # 2) Config dentro de .jsdos/
    z.write(os.path.join(bundle_dir, "dosbox.conf"), ".jsdos/dosbox.conf")

    # 3) Override corto en la raíz (como el bundle oficial)
    z.writestr("dosbox.conf", "[cpu]\r\ncycles=fixed 30000\r\n")

    # 4) Juego en la raíz
    for name in sorted(os.listdir(bundle_dir)):
        if name in skip:
            continue
        p = os.path.join(bundle_dir, name)
        if os.path.isfile(p):
            z.write(p, name)

# Verificación
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
print("tamano: %.1f MB" % (os.path.getsize(out) / 1024 / 1024))
sys.exit(0 if ok else 1)
