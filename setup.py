from cx_Freeze import setup, Executable
import sys

base = "Win32GUI" if sys.platform == "win32" else None
icon_file = "logo.ico"

build_exe_options = {
    "include_files": [icon_file],
}

msi_options = {
    "upgrade_code": "{F7A2E5C3-9D4E-4A8C-9B8D-7A1234567890}",
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\GameSense",
}

setup(
    name="GameSense",
    version="1.0.0",
    description="Приложение для клуба",
    author="falbue",
    author_email="cyansair05@gmail.com",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": msi_options,
    },
    executables=[
        Executable(
            script="app.py",
            base=base,
            icon=icon_file,
            target_name="GameSense.exe",
            shortcut_name="GameSense",
            shortcut_dir="DesktopFolder",
        )
    ],
)