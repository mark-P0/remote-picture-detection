import sys  # noqa
import os

from kivy_deps import sdl2, glew
from kivymd import hooks_path as kivymd_hooks_path


EXENAME = 'Server UI'

path = os.path.abspath('.')

data_files = [
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/data", "data"),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/images", "images"),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/scripts", "scripts/"),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/ui", "ui/"),

    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/main.py", "."),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/main.kv", "."),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/server.py", "."),
    ("C:/Users/Mark/Documents/__projects/__python_venvs/http-practice/faces.py", "."),

    ('./fr_models/models/dlib_face_recognition_resnet_model_v1.dat', './face_recognition_models/models'),  # noqa
    ('./fr_models/models/mmod_human_face_detector.dat', './face_recognition_models/models'),
    ('./fr_models/models/shape_predictor_5_face_landmarks.dat', './face_recognition_models/models'),  # noqa
    ('./fr_models/models/shape_predictor_68_face_landmarks.dat', './face_recognition_models/models'),  # noqa
]


a = Analysis(  # noqa
    ['main.py'],
    pathex=[path],
    # binaries=face_models,  # For the face recognition models?
    datas=data_files,
    hiddenimports=['face_recognition', 'face_recognition_models'],
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
