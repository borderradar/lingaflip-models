#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# LingaFlip — GitHub LFS Push Script
# Run this in your terminal on your Mac, from the lingaflip-models folder.
#
# Prerequisites:
#   brew install git-lfs   (one time)
#   gh auth login          (one time — or set up SSH key on GitHub)
# ─────────────────────────────────────────────────────────────────────────────

set -e  # Stop on any error

REPO="https://github.com/borderradar/lingaflip-models.git"
BRANCH="main"

echo "================================================"
echo "  LingaFlip — GitHub LFS Push"
echo "================================================"

# ── 1. Check git-lfs is installed ──────────────────────────────────────────
if ! command -v git-lfs &> /dev/null; then
  echo ""
  echo "❌  git-lfs not found. Install it first:"
  echo "      brew install git-lfs"
  echo ""
  exit 1
fi
echo "✅  git-lfs found: $(git-lfs version)"

# ── 2. Initialise git-lfs for this user (safe to run multiple times) ───────
git lfs install
echo "✅  git-lfs initialised"

# ── 3. Init git repo if needed ─────────────────────────────────────────────
if [ ! -d ".git" ]; then
  git init -b "$BRANCH"
  echo "✅  Git repository initialised"
else
  echo "✅  Git repository already exists"
fi

# ── 4. Set remote ──────────────────────────────────────────────────────────
if git remote get-url origin &> /dev/null; then
  git remote set-url origin "$REPO"
  echo "✅  Remote 'origin' updated to $REPO"
else
  git remote add origin "$REPO"
  echo "✅  Remote 'origin' added: $REPO"
fi

# ── 5. Stage everything (respects .gitignore and .gitattributes) ───────────
echo ""
echo "Staging files..."
git add .
echo ""

# ── 6. Show what will be committed ─────────────────────────────────────────
echo "── Files staged ──────────────────────────────"
git status --short
echo ""
echo "── LFS tracked files ─────────────────────────"
git lfs status 2>/dev/null || echo "(none yet — will be tracked on push)"
echo ""

# ── 7. Confirm before push ─────────────────────────────────────────────────
read -p "Ready to commit and push to $REPO ? [y/N] " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "Aborted."
  exit 0
fi

# ── 8. Commit ──────────────────────────────────────────────────────────────
git commit -m "Add LingaFlip TTS voice models (8 languages, Piper ONNX + manifests)"

# ── 9. Push (LFS objects upload automatically) ─────────────────────────────
echo ""
echo "Pushing to GitHub (LFS objects will upload automatically)..."
echo "This may take a few minutes for the .onnx files (~500 MB total)."
echo ""
git push -u origin "$BRANCH"

echo ""
echo "================================================"
echo "  ✅  Done! Repository pushed to:"
echo "      $REPO"
echo "================================================"
echo ""
echo "⚠️  Still to do manually:"
echo "  1. Download Chinese voice (MeloTTS MIT):"
echo "     cd voices/zh_CN"
echo "     curl -L -O https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-melo-tts-zh_en.tar.bz2"
echo "     tar xvf vits-melo-tts-zh_en.tar.bz2 && mv vits-melo-tts-zh_en melo && rm *.tar.bz2"
echo ""
echo "  2. Download Japanese voice (Kokoro Apache 2.0):"
echo "     See VOICE_SELECTION.md → Japanese section"
echo ""
echo "  3. Delete voices/zh_CN/huayan/ (unknown license — do not push)"
echo "     Already excluded by .gitignore — just delete the folder when convenient."
echo ""
