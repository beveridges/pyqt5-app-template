# PyQt5 App Template

**Version:** 25.11-alpha.01  
**Author:** Scott Beveridge  
**License:** MIT  

## 🧩 Release Workflow — MOTUS / Application Template

This section describes the full lifecycle for building, tagging, and publishing releases for the **MOTUS Application Template**.

---

### 1️⃣ Development & Testing Phase

During development:
```bash
git add .
git commit -m "Implement new plotting overlay system"
```

To test your current build as a portable executable:
```bash
python build_template.py
```
or if you’ve made a helper script:
```bash
./build_template.sh
```

> This produces a portable executable under `dist/`, ideal for quick testing on other systems.

---

### 2️⃣ Preparing a Release Candidate

Once the portable build is stable:

1. **Freeze your changes:**
   ```bash
   git status
   git add .
   git commit -m "Finalize v25.11-alpha.01.00 portable build"
   ```

2. **Create a release tag:**
   ```bash
   git tag -a v25.11-alpha.01.00 -m "Alpha release candidate for MOTUS"
   git push origin v25.11-alpha.01.00
   ```

> Tags mark a specific snapshot in Git — your official “release point.”

---

### 3️⃣ Building the MSI Installer

Once tagged, build the MSI:

```bash
python build_template_msi.py
```
or with your shell wrapper:
```bash
./build_msi.sh
```

This should:
- Pull the version info from `version_info.py` or `git describe`
- Output a `.msi` file under `dist/`, for example:
  ```
  dist/MOTUS_Setup_v25.11-alpha.01.00.msi
  ```

---

### 4️⃣ Creating a GitHub Release

Once the MSI is verified:

1. Go to your GitHub repository → **Releases** → **Draft a new release**
2. Choose your tag (e.g. `v25.11-alpha.01.00`)
3. Fill in:
   - **Title:** `MVC Calculator v25.11-alpha.01.00`
   - **Notes:** Summary of new features or fixes
4. Attach both files:
   - `MVC_Calculator_Portable_v25.11-alpha.01.00.zip`
   - `MVC Calculator_setup_v25.11-alpha.01.00.msi`
5. Click **“Publish Release”**

---

### 5️⃣ Automating the Process

You can simplify the process with a release script named `release_build.sh`:

```bash
#!/bin/bash
# release_build.sh — build, tag, and prepare GitHub release

VERSION="25.11-alpha.01.00"
MESSAGE="Release $VERSION"

echo "🔧 Building portable executable..."
python build_template.py || exit 1

echo "🏷️  Creating git tag v$VERSION..."
git add .
git commit -m "$MESSAGE"
git tag -a "v$VERSION" -m "$MESSAGE"
git push origin main --tags

echo "📦 Building MSI installer..."
python build_template_msi.py || exit 1

echo "✅ All done! Go to GitHub → Releases → 'Draft new release' → Select tag v$VERSION"
```

If you have the **GitHub CLI** installed, you can also publish directly:

```bash
gh release create "v$VERSION" dist/*.msi dist/*.zip \
  --title "MOTUS $VERSION" \
  --notes "$MESSAGE"
```

---

### 6️⃣ Summary Flow

| Step | Action | Script |
|------|---------|--------|
| Develop & test | Build portable executable | `build_template.py` |
| Freeze | Commit + tag release | `git tag -a vX.Y` |
| Build installer | Generate `.msi` | `build_template_msi.py` |
| Publish | Upload to GitHub | `release_build.sh` or `gh release create` |



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
