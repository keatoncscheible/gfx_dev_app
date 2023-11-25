import os
import re

app_folder = "src/pyfx"
ui_folder = "ui"
resources_folder = "resources"


def fix_transport_control_icons_import():
    transport_control_ui_file = os.path.join(app_folder, ui_folder, "transport_control_widget_ui.py")
    new_icon_import = "import pyfx.assets.icons_rc\n"

    with open(transport_control_ui_file) as file:
        transport_control_ui_file_contents = file.read()

    old_icon_import_regex = r"import\s+icons_rc\s*\n"
    new_transport_control_ui_file_contents = re.sub(
        old_icon_import_regex,
        new_icon_import + "\n",
        transport_control_ui_file_contents,
    )

    with open(transport_control_ui_file, "w") as file:
        file.write(new_transport_control_ui_file_contents)


for filename in os.listdir(f"{app_folder}/{ui_folder}"):
    root, ext = os.path.splitext(filename)
    if ext == ".ui":
        generated_py_ui_file = f"{root}_ui.py"
        print(f"Generating {generated_py_ui_file}")
        os.system(
            f".venv\\Scripts\\python.exe .venv\\Scripts\\pyside6-uic.exe {app_folder}\\{ui_folder}\\{root}.ui -o {app_folder}\\{ui_folder}\\{generated_py_ui_file}"
        )

fix_transport_control_icons_import()
