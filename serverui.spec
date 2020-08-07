import sys  # noqa
import os

from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path


EXENAME = 'Server UI'

path = os.path.abspath('.')

data_files = [
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/images", "images"),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/received", "received"),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/ui", "ui/"),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/scripts", "scripts/"),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/main.py", "."),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/main.kv", "."),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/server.py", "."),
]


a = Analysis(  # noqa
    ['main.py'],
    pathex=[path],
    datas=data_files,
    hookspath=[kivymd_hooks_path],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(  # noqa
    a.pure,
    a.zipped_data,
    cipher=None
)

exe = EXE(  # noqa
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],  # noqa
    debug=False,
    strip=False,
    upx=True,
    name=EXENAME,
    console=True,
)

coll = COLLECT(  # noqa
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=EXENAME,
)
