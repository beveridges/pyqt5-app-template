#!/bin/bash
# ======================================================================
# setup_template_env.sh
# Create or rebuild a Conda environment for Motus / OpenSim projects.
#
# Usage:
#   source setup_template_env.sh [env_name] [-a]
#
# Example:
#   source setup_template_env.sh environment_template -a
# ======================================================================

set -e  # exit on first error
set -o pipefail

# --- Enable conda for non-interactive shell ---
if ! command -v conda &>/dev/null; then
    echo "⚠️ Conda not found in PATH — attempting to source it..."
    source "$(conda info --base)/etc/profile.d/conda.sh" || {
        echo "❌ Failed to initialize conda. Please start from an Anaconda Prompt or source conda.sh manually."
        exit 1
    }
else
    source "$(conda info --base)/etc/profile.d/conda.sh"
fi

# --- Parse arguments ---
ENV_NAME=${1:-motus_osim4511}
ACTIVATE_AFTER=false

if [[ "$2" == "-a" || "$1" == "-a" ]]; then
    ACTIVATE_AFTER=true
fi

# --- Setup logging ---
LOGFILE="setup_${ENV_NAME}_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -i "$LOGFILE") 2>&1

echo "=============================================================="
echo "  🧩 Setting up Conda environment: $ENV_NAME"
echo "  📄 Logging all output to: $LOGFILE"
echo "=============================================================="
sleep 1

# --- Create environment ---
echo "🚀 Creating environment with Python 3.10.18..."
conda create -y -n "$ENV_NAME" python=3.10.18

# --- Activate environment for installation ---
echo "🔄 Activating environment..."
conda activate "$ENV_NAME"

# --- Install core dependencies ---
echo "📦 Installing core dependencies..."
conda install -y spyder-kernels=3.0
conda install -y -c conda-forge pyqt=5
conda install -y -c opensim-org opensim=4.5.1
conda install -y -c conda-forge matplotlib=3.10.0
conda install -y -c conda-forge pandas=2.2.3
conda install -y -c conda-forge openpyxl=3.1.5
pip install pyinstaller==6.16.0
conda install -y -c conda-forge pytest-qt
conda install -y -c conda-forge pytest-cov pytest-sugar
pip install mkdocs
pip install mkdocs-bibtex

# --- Export environment snapshot ---
EXPORT_FILE="${ENV_NAME}_export.yml"
echo "🧾 Exporting environment to $EXPORT_FILE..."
conda env export --no-builds > "$EXPORT_FILE"

echo "✅ Environment '$ENV_NAME' created and exported successfully!"
echo "📦 Environment snapshot: $EXPORT_FILE"
echo "🪵 Log file: $LOGFILE"

# --- Optional activation ---
if $ACTIVATE_AFTER; then
    echo "🔌 Activating environment '$ENV_NAME'..."
    conda activate "$ENV_NAME"
    echo "✅ Environment '$ENV_NAME' is now active."
else
    echo "💡 To activate later, run: conda activate $ENV_NAME"
fi

echo "=============================================================="
echo "🎉 Setup complete for '$ENV_NAME'!"
echo "=============================================================="
