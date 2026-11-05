#!/bin/sh
# Réinitialisation de l'environnement (le sandbox peut être recréé entre deux tours).
# Usage :  sh work/setup.sh
set -e
cd "$(dirname "$0")/.."
if ! .venv/bin/python -c "import pymupdf" 2>/dev/null; then
    [ -d .venv ] || python3 -m venv .venv
fi
.venv/bin/python -m pip install -q --disable-pip-version-check pymupdf python-docx pillow
echo "OK pymupdf $(.venv/bin/python -c 'import pymupdf;print(pymupdf.__version__)')"
