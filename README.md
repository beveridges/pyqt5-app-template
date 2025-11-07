# PyQt5 App Template

**Version:** 25.11-alpha.01  
**Author:** Scott Beveridge  
**License:** MIT  

A modern, production-ready **PyQt5 application skeleton** featuring:

- ✅ Pre-wired **UI loading** via `ui_initializer.py`
- ✅ Integrated **MkDocs documentation** (ReadTheDocs theme)
- ✅ Safe **build system** using `build_template.py`
- ✅ Structured resources, icons, and version tracking
- ✅ Optional early splash screen and logging system

---

## 🚀 Quick Start

### 1. Clone this repository

```bash
git clone https://github.com/beveridges/pyqt5-app-template.git
cd pyqt5-app-template
```

### 2. When ready to build

```bash
python build_template.py
python build_template_msi.py
```

---

## 🧩 Features

| Feature | Description |
|----------|-------------|
| 🪶 **UI Loading System** | Pre-connected UI loader for `.ui` files via `ui_initializer.py`. |
| 📦 **Build Scripts** | Two build scripts included — one for **portable EXE** and one for **MSI installers**. |
| 🧰 **Resources Structure** | Icons, splash screens, and templates are organized under `/resources`. |
| 📚 **Documentation** | Built-in MkDocs configuration with ReadTheDocs theme. |
| ⚙️ **Version Tracking** | Automatic semantic versioning in `utilities/version_info.py`. |
| 💬 **Logging System** | Optional RotatingFileHandler for persistent logging. |

---

## 🧱 Project Structure

```
pyqt5-app-template/
├── build_template.py
├── build_template_msi.py
├── docs_site/
│   ├── docs/
│   │   ├── index.md
│   │   ├── getting_started.md
│   │   ├── usage.md
│   │   └── configuration.md
│   └── mkdocs.yml
├── main.py
├── resources/
│   ├── icons/
│   │   ├── app.ico
│   │   ├── icon.png
│   │   └── splash.png
│   └── data/
├── utilities/
│   ├── version_info.py
│   └── path_utils.py
└── README.md
```

---

## 🧰 Build Options

### 🖥 Portable Build (EXE)
Builds a standalone **EXE folder** using PyInstaller.

```bash
python build_template.py
```

Output example:
```
C:\Users\Scott\Documents\.builds\myapptemplate\pyinstaller\dist\MyAppTemplate\
```

### 📦 Installer Build (MSI)
Creates a Windows Installer (`.msi`) using the WiX Toolset.

```bash
python build_template_msi.py
```

Output example:
```
C:\Users\Scott\Documents\.builds\myapptemplate\msi\builds\
│
├─ MyAppTemplate-25.11-alpha.01.07.msi
├─ MyAppTemplate-25.11-alpha.01.07-portable.zip
```

---

## 🧭 Usage Notes

- All paths resolve dynamically using `utilities/path_utils.py` and `base_path()`.
- `version_info.py` is automatically updated on each build.
- The splash screen and logging system are optional — you can disable them via the app’s configuration.
- The MSI build automatically includes your icon, desktop shortcut, and uninstall registry entries.

---

## 🪄 Tips

- For **new projects**, clone this repo as a base template:
  ```bash
  git clone https://github.com/beveridges/pyqt5-app-template.git new_app
  cd new_app
  git remote remove origin
  git init
  ```
- Then rename your app and start development.
- Optional: add your own company name and version in `build_template_msi.py`.

---

## 🧑‍💻 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
