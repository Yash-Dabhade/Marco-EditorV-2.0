from cx_Freeze import setup,Executable
import os

import sys

if sys.platform == 'win32':
    basew = 'Win32GUI'

os.environ['TCL_LIBRARY'] = r"C:\Users\yash\AppData\Local\Programs\Python\Python37\tcl\tcl8.6 "
os.environ['TK_LIBRARY'] = r"C:\Users\yash\AppData\Local\Programs\Python\Python37\tcl\tk8.6"

#executable= [cx_Freeze.Executable("MarcoEditor.py", base=basew, icon="icon.ico")]

setup(

    name="MarcoEditor",
    options={"build_exe": {"packages": ["tkinter", "os"],
                           "include_files": ["icon.ico", "menu_icons", "icons2", "icons", "tcl86t.dll", "tk86t.dll"]}},
    version="2.0",
    description="A Text Editor made by YASH DABHADE",
    executables= [Executable("MarcoEditor.py", base=basew, icon="icon.ico")]

)
