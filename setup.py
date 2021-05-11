""" setup for cx_freeze

    usage: python setup.py bdist_msi

"""

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "include_files": ["wse_investor\\limits.yaml"]}

# GUI applications require a different base on Windows (the default is for
# a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="wse_investor",
    version="0.1",
    description="WSE Investor.",
    options={"build_exe": build_exe_options},
    executables=[Executable("wse_investor\\_gui.py", base=base)]
)