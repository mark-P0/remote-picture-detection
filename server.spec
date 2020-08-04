import sys
import os

from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path


path = os.path.abspath('.')

data_files = [
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/images", "images" ),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/received", "received"),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/widgets", "widgets/"),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/main.py", "."),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/serverui.kv", "."),
]

# --add-data "C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/images;images/" 
# --add-data "C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/received;received/" 
# --add-data "C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/widgets;widgets/" 
# --add-data "C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/main.py;." 
# --add-data "C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/serverui.kv;." 

app_name = 'Server UI'

a = Analysis(
    ['server.py'],
    pathex=[path],
    datas=data_files,
    hookspath=[kivymd_hooks_path],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    debug=False,
    strip=False,
    upx=True,
    name=app_name,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name,
)