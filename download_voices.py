#!/usr/bin/env python3
"""
LingaFlip — Piper TTS Voice Downloader
=======================================
Run this script on your local machine to download all selected voice models.
Downloaded files go into ./voices/ ready to push to GitHub.

Usage:
    pip install requests tqdm
    python download_voices.py

Requirements: Python 3.8+, ~250 MB disk space
"""

import os
import sys
import hashlib
import requests
from pathlib import Path

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    print("Tip: install tqdm for a progress bar → pip install tqdm")

# ─────────────────────────────────────────────────────────────────────────────
# VOICE SELECTION
# Each entry: (output_dir, hf_path_prefix, filename_base, license_note)
#
# HuggingFace base URL:
#   https://huggingface.co/rhasspy/piper-voices/resolve/main/<hf_path_prefix>/
# ─────────────────────────────────────────────────────────────────────────────

HF_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

VOICES = [
    {
        "lang":        "en_US",
        "voice":       "ljspeech",
        "quality":     "high",
        "hf_path":     "en/en_US/ljspeech/high",
        "license":     "MIT — no attribution required ✅",
        "note":        "Best English US female voice (LJSpeech dataset)"
    },
    {
        "lang":        "en_GB",
        "voice":       "alba",
        "quality":     "medium",
        "hf_path":     "en/en_GB/alba/medium",
        "license":     "CC0 1.0 — no attribution required ✅",
        "note":        "Scottish English female voice"
    },
    {
        "lang":        "de_DE",
        "voice":       "thorsten",
        "quality":     "high",
        "hf_path":     "de/de_DE/thorsten/high",
        "license":     "CC0 1.0 — no attribution required ✅",
        "note":        "Gold-standard open German voice (Thorsten)"
    },
    {
        "lang":        "fr_FR",
        "voice":       "siwis",
        "quality":     "medium",
        "hf_path":     "fr/fr_FR/siwis/medium",
        "license":     "MIT — no attribution required ✅ (verify MODEL_CARD)",
        "note":        "Swiss French female voice, avoids NC-licensed upmc"
    },
    {
        "lang":        "it_IT",
        "voice":       "paola",
        "quality":     "medium",
        "hf_path":     "it/it_IT/paola/medium",
        "license":     "CC0 1.0 — no attribution required ✅",
        "note":        "Best Italian female voice"
    },
    {
        "lang":        "ru_RU",
        "voice":       "irina",
        "quality":     "medium",
        "hf_path":     "ru/ru_RU/irina/medium",
        "license":     "CC-BY-SA 4.0 ⚠️ — voice data from RHVoice; credit: 'Irina, RHVoice, CC-BY-SA 4.0'; commercial use OK",
        "note":        "Natural Russian female voice"
    },
    {
        "lang":        "tr_TR",
        "voice":       "dfki",
        "quality":     "medium",
        "hf_path":     "tr/tr_TR/dfki/medium",
        "license":     "MIT — no attribution required ✅",
        "note":        "DFKI Turkish voice (fahrettin/fettah were removed from the repo)"
    },
    # zh_CN-huayan EXCLUDED: source repo PlayVoice/HuaYan_TTS is deleted (404),
    # license is Unknown — legally unsafe for commercial use.
    # Chinese is handled separately below via MeloTTS (MIT).

    {
        "lang":        "es_ES",
        "voice":       "davefx",
        "quality":     "medium",
        "hf_path":     "es/es_ES/davefx/medium",
        "license":     "MIT — no attribution required ✅",
        "note":        "Spain Spanish male voice (user-selected, MIT license)"
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Japanese: Kokoro TTS (Apache 2.0) — NOT from Piper repo
# This is a SEPARATE download step. Kokoro uses a different integration.
# ─────────────────────────────────────────────────────────────────────────────

MELOTTS_NOTE = """
🇨🇳  CHINESE VOICE — MeloTTS (MIT License)
==========================================
zh_CN-huayan was EXCLUDED: its source repo (PlayVoice/HuaYan_TTS) is deleted
and the license is Unknown — not safe for commercial use.

Instead, use MeloTTS-Chinese (MIT, higher quality):

  Run these commands in your terminal:
    cd voices/zh_CN
    curl -L -O https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-melo-tts-zh_en.tar.bz2
    tar xvf vits-melo-tts-zh_en.tar.bz2
    mv vits-melo-tts-zh_en melo
    rm vits-melo-tts-zh_en.tar.bz2

  Source:  https://huggingface.co/myshell-ai/MeloTTS-Chinese
  License: MIT — no attribution required ✅
  Note:    Supports Chinese + English mixed speech (ideal for a language learning app)

"""

KOKORO_NOTE = """
⚠️  JAPANESE VOICE — Manual Download Required
==============================================
Piper has no official Japanese voice. Use Kokoro TTS instead:

  Model: hexgrad/Kokoro-82M (Apache 2.0 — no attribution required)
  ONNX:  onnx-community/Kokoro-82M-v1.0-ONNX

  Steps:
  1. Visit: https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX
  2. Download: kokoro-v1.0.onnx  (or the quantized version for smaller size)
  3. Place in:  voices/ja_JP/kokoro/
  4. Integration differs from Piper — see REACT_NATIVE_GUIDE.md

"""


def download_file(url: str, dest: Path, label: str) -> bool:
    """Download a file with progress display. Returns True on success."""
    try:
        response = requests.get(url, stream=True, timeout=60,
                                headers={"User-Agent": "LingaFlip-voice-downloader/1.0"})
        if response.status_code == 404:
            print(f"  ✗ NOT FOUND (404): {url}")
            print(f"    → Check the HuggingFace repo manually: https://huggingface.co/rhasspy/piper-voices")
            return False
        response.raise_for_status()

        total = int(response.headers.get("content-length", 0))
        dest.parent.mkdir(parents=True, exist_ok=True)

        if HAS_TQDM and total > 0:
            with open(dest, "wb") as f, tqdm(
                desc=f"  {label}",
                total=total,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bar.update(len(chunk))
        else:
            print(f"  Downloading {label} ...", end="", flush=True)
            with open(dest, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            mb = os.path.getsize(dest) / (1024 * 1024)
            print(f" {mb:.1f} MB ✓")

        return True

    except requests.RequestException as e:
        print(f"  ✗ Error downloading {url}: {e}")
        return False


def download_voice(voice: dict, output_base: Path) -> bool:
    lang = voice["lang"]
    name = voice["voice"]
    quality = voice["quality"]
    hf_path = voice["hf_path"]

    file_base = f"{lang}-{name}-{quality}"
    output_dir = output_base / lang / name

    print(f"\n{'─'*60}")
    print(f"  Language : {lang}")
    print(f"  Voice    : {name} ({quality})")
    print(f"  License  : {voice['license']}")
    print(f"  Note     : {voice['note']}")
    print(f"{'─'*60}")

    success = True

    # 1. Download ONNX model
    onnx_url  = f"{HF_BASE}/{hf_path}/{file_base}.onnx"
    onnx_dest = output_dir / f"{file_base}.onnx"

    if onnx_dest.exists():
        print(f"  ✓ Already exists: {onnx_dest.name} (skipping)")
    else:
        ok = download_file(onnx_url, onnx_dest, f"{file_base}.onnx")
        success = success and ok

    # 2. Download JSON config
    json_url  = f"{HF_BASE}/{hf_path}/{file_base}.onnx.json"
    json_dest = output_dir / f"{file_base}.onnx.json"

    if json_dest.exists():
        print(f"  ✓ Already exists: {json_dest.name} (skipping)")
    else:
        ok = download_file(json_url, json_dest, f"{file_base}.onnx.json")
        success = success and ok

    # 3. Download MODEL_CARD (license file — important!)
    card_url  = f"{HF_BASE}/{hf_path}/MODEL_CARD"
    card_dest = output_dir / "MODEL_CARD.txt"

    if card_dest.exists():
        print(f"  ✓ Already exists: MODEL_CARD.txt (skipping)")
    else:
        ok = download_file(card_url, card_dest, "MODEL_CARD.txt")
        # Non-fatal if missing
        if not ok:
            print("    (MODEL_CARD not found — check license manually on HuggingFace)")

    return success


def main():
    print("=" * 60)
    print("  LingaFlip — Piper TTS Voice Downloader")
    print("  Target: voices/ folder → push to GitHub")
    print("=" * 60)

    output_base = Path("voices")
    output_base.mkdir(exist_ok=True)

    failed = []

    for voice in VOICES:
        ok = download_voice(voice, output_base)
        if not ok:
            failed.append(voice["lang"])

    # Print summary
    print("\n" + "=" * 60)
    print("  DOWNLOAD SUMMARY")
    print("=" * 60)

    if failed:
        print(f"\n  ⚠️  Failed languages: {', '.join(failed)}")
        print("     → Check the HuggingFace repo for correct paths:")
        print("       https://huggingface.co/rhasspy/piper-voices/tree/main")
    else:
        print("\n  ✅ All Piper voices downloaded successfully!")

    print(MELOTTS_NOTE)
    print(KOKORO_NOTE)

    # Print attribution reminder
    print("─" * 60)
    print("  CC-BY 4.0 ATTRIBUTION — Add to your release notes:")
    print("─" * 60)
    print("""
  Voice Credits:
  - Russian: Irina voice, © RHVoice (github.com/RHVoice/RHVoice), CC-BY-SA 4.0
  Japanese: Kokoro (hexgrad/Kokoro-82M), Apache 2.0
    """)

    print("─" * 60)
    print("  Next steps:")
    print("  1. Verify MODEL_CARD.txt for each voice (especially zh_CN)")
    print("  2. git add voices/ && git commit -m 'Add TTS voice models'")
    print("  3. git push origin main")
    print("─" * 60)


if __name__ == "__main__":
    main()
