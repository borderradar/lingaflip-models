# LingaFlip — Piper TTS Voice Selection Guide

> **Repository:** https://github.com/borderradar/lingaflip-models  
> **Source:** https://huggingface.co/rhasspy/piper-voices/tree/main  
> **Last reviewed:** April 2026

---

## License Key

| Symbol | Meaning |
|--------|---------|
| ✅ CC0 / MIT / Apache 2.0 | Fully free — no attribution required |
| ⚠️ CC-BY 4.0 | Free to use commercially — **must credit the voice author in your release notes / about screen** |
| ❌ CC-BY-NC / CC-BY-SA | Restricted or share-alike — **avoid for a commercial app** |

> **Important:** Always open the `MODEL_CARD` file inside each voice's folder on HuggingFace before final shipping to confirm the license has not changed. The URLs are listed in the download script.

---

## Selected Voices — One Per Language

### 🇺🇸 English (United States)
| Field | Value |
|-------|-------|
| Voice ID | `en_US-ljspeech-high` |
| Quality | **High** ⭐⭐⭐ |
| Gender | Female |
| License | ✅ **MIT** — No attribution required |
| Why chosen | LJSpeech is a public-domain audiobook dataset. Clean, neutral American accent. Best quality available with no legal restrictions. |
| ONNX file | `en/en_US/ljspeech/high/en_US-ljspeech-high.onnx` (~63 MB) |
| Config file | `en/en_US/ljspeech/high/en_US-ljspeech-high.onnx.json` |
| MODEL_CARD | `en/en_US/ljspeech/high/MODEL_CARD` |

---

### 🇬🇧 English (United Kingdom)
| Field | Value |
|-------|-------|
| Voice ID | `en_GB-alba-medium` |
| Quality | **Medium** ⭐⭐⭐ |
| Gender | Female |
| License | ✅ **CC0 1.0** — No attribution required |
| Why chosen | Clear Scottish-English accent. CC0 (public domain) license. Good fallback for British English learners. |
| ONNX file | `en/en_GB/alba/medium/en_GB-alba-medium.onnx` (~15 MB) |
| Config file | `en/en_GB/alba/medium/en_GB-alba-medium.onnx.json` |
| MODEL_CARD | `en/en_GB/alba/medium/MODEL_CARD` |

---

### 🇩🇪 German
| Field | Value |
|-------|-------|
| Voice ID | `de_DE-thorsten-high` |
| Quality | **High** ⭐⭐⭐ |
| Gender | Male |
| License | ✅ **CC0 1.0** — No attribution required |
| Why chosen | Thorsten is the gold-standard open German TTS voice. CC0 license. Natural prosody, very clear articulation — ideal for language learners. |
| ONNX file | `de/de_DE/thorsten/high/de_DE-thorsten-high.onnx` (~63 MB) |
| Config file | `de/de_DE/thorsten/high/de_DE-thorsten-high.onnx.json` |
| MODEL_CARD | `de/de_DE/thorsten/high/MODEL_CARD` |

---

### 🇫🇷 French
| Field | Value |
|-------|-------|
| Voice ID | `fr_FR-siwis-medium` |
| Quality | **Medium** ⭐⭐⭐ |
| Gender | Female |
| License | ✅ **MIT** — No attribution required |
| Why chosen | SIWIS (Swiss French) dataset — clean, neutral French accent. High intelligibility. Avoids the fr_FR-upmc voice which is CC-BY-NC (non-commercial). |
| ONNX file | `fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx` (~15 MB) |
| Config file | `fr/fr_FR/siwis/medium/fr_FR-siwis-medium.onnx.json` |
| MODEL_CARD | `fr/fr_FR/siwis/medium/MODEL_CARD` |
| ⚠️ Note | Verify MODEL_CARD confirms MIT before shipping. Avoid `fr_FR-upmc` (CC-BY-NC = non-commercial only). |

---

### 🇮🇹 Italian
| Field | Value |
|-------|-------|
| Voice ID | `it_IT-paola-medium` |
| Quality | **Medium** ⭐⭐ |
| Gender | Female |
| License | ✅ **CC0 1.0** — No attribution required |
| Why chosen | Best Italian voice in the repository. Natural intonation. |
| ONNX file | `it/it_IT/paola/medium/it_IT-paola-medium.onnx` (~15 MB) |
| Config file | `it/it_IT/paola/medium/it_IT-paola-medium.onnx.json` |
| MODEL_CARD | `it/it_IT/paola/medium/MODEL_CARD` |

---

### 🇷🇺 Russian
| Field | Value |
|-------|-------|
| Voice ID | `ru_RU-irina-medium` |
| Quality | **Medium** ⭐⭐⭐ |
| Gender | Female |
| License | ⚠️ **CC-BY-SA 4.0** — Attribution + ShareAlike required |
| Source | Voice data originates from **RHVoice** (https://github.com/RHVoice/RHVoice) |
| Why chosen | Irina is the most natural-sounding Russian Piper voice. Clear articulation, good for learning. Denis and Dmitri are also good male options. |
| ONNX file | `ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx` (~15 MB) |
| Config file | `ru/ru_RU/irina/medium/ru_RU-irina-medium.onnx.json` |
| MODEL_CARD | `ru/ru_RU/irina/medium/MODEL_CARD` |
| ⚠️ Attribution | Add to app credits: *"Russian voice: Irina, © RHVoice (https://github.com/RHVoice/RHVoice), CC-BY-SA 4.0"* |
| ℹ️ ShareAlike note | ShareAlike applies to the **model files only** — not your app code. You may use the voice commercially. If you redistribute the `.onnx` file, keep the CC-BY-SA 4.0 license notice alongside it (which your GitHub repo should include). |

---

### 🇹🇷 Turkish
| Field | Value |
|-------|-------|
| Voice ID | `tr_TR-dfki-medium` |
| Quality | **Medium** ⭐⭐ |
| Gender | Male |
| License | ✅ **MIT** — No attribution required |
| Why chosen | DFKI (German Research Center for AI) Turkish voice. `fahrettin` and `fettah` were **removed** from the piper-voices repo — dfki is the only currently available Turkish voice. MIT license confirmed via MODEL_CARD. |
| ONNX file | `tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx` (~15 MB) |
| Config file | `tr/tr_TR/dfki/medium/tr_TR-dfki-medium.onnx.json` |
| MODEL_CARD | `tr/tr_TR/dfki/medium/MODEL_CARD` |

---

### 🇨🇳 Chinese (Mandarin)
| Field | Value |
|-------|-------|
| Voice ID | `vits-melo-tts-zh_en` |
| Quality | **High** ⭐⭐⭐ |
| Gender | Female |
| License | ✅ **MIT** — No attribution required |
| Engine | **MeloTTS** (not Piper) — pre-converted to ONNX by sherpa-onnx |
| Why chosen | `zh_CN-huayan` was removed — its source repo (PlayVoice/HuaYan_TTS) is deleted (404) and the license is **Unknown**, making it legally unsafe for commercial use (see [piper issue #818](https://github.com/rhasspy/piper/issues/818)). MeloTTS-Chinese is MIT licensed, higher quality, and supports Chinese+English mixed speech. |
| Source | https://huggingface.co/myshell-ai/MeloTTS-Chinese (MIT) |
| ONNX download | `https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-melo-tts-zh_en.tar.bz2` |
| Place files in | `voices/zh_CN/melo/` |
| ℹ️ Integration | Uses same sherpa-onnx runtime. See `REACT_NATIVE_GUIDE.md` for the MeloTTS config. |

---

### 🇯🇵 Japanese — ⚠️ NOT Available in Piper
| Status | No official `ja_JP` voice exists in the rhasspy/piper-voices repository |
|--------|------|

**Recommended Alternative: Kokoro TTS (Apache 2.0)**

Kokoro is an open-weight ONNX model with excellent Japanese support:
- 🔗 Model: https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX
- License: **Apache 2.0** ✅ — No attribution required for commercial use
- Japanese voice: `jf_alpha` (Japanese Female)
- Quality: High — comparable to commercial TTS
- File format: ONNX (compatible with the same runtime)
- Note: Uses a different voices.json format than Piper. Integration guide in the React Native section.

---

### 🇪🇸 Spanish
| Field | Value |
|-------|-------|
| Voice ID | `es_ES-davefx-medium` |
| Quality | **Medium** ⭐⭐⭐ |
| Gender | Male |
| License | ✅ **MIT** — No attribution required |
| Why chosen | Spain Spanish, user-selected. MIT license — no attribution needed. |
| ONNX file | `es/es_ES/davefx/medium/es_ES-davefx-medium.onnx` (~63 MB) |
| Config file | `es/es_ES/davefx/medium/es_ES-davefx-medium.onnx.json` |
| MODEL_CARD | `es/es_ES/davefx/medium/MODEL_CARD` |

---

## Attribution Template for Release Notes / About Screen

For the CC-BY-SA 4.0 Russian voice, include this in your app's credits / About screen:

```
Voice Attribution:
- Russian: Irina voice, © RHVoice (https://github.com/RHVoice/RHVoice), CC-BY-SA 4.0
  Model files redistributed under the same CC-BY-SA 4.0 license.

Japanese TTS: Kokoro (hexgrad/Kokoro-82M), Apache 2.0
Piper TTS engine: https://github.com/rhasspy/piper (MIT)
```

---

## Voices NOT Selected — Reasons

| Voice | Reason Excluded |
|-------|----------------|
| `fr_FR-upmc-medium` | CC-BY-NC-SA 4.0 — Non-commercial only ❌ |
| `zh_CN-huayan-medium` | Source repo deleted (PlayVoice/HuaYan_TTS is 404), license Unknown ❌ |
| `tr_TR-fahrettin-medium` | Removed from piper-voices repo — no longer available |
| `tr_TR-fettah-medium` | Removed from piper-voices repo — no longer available |
| `ru_RU-ruslan-medium` | License uncertain / may be CC-BY-NC ❌ |
| `en_US-lessac-high` | Blizzard Challenge dataset — commercial use requires review ❌ |
| `de_DE-kerstin-low` | Low quality only |
| `es_ES-carlfm-x_low` | X-Low quality — too robotic for language learning |

---

## File Size Summary

| Language | Voice | Quality | Est. Size |
|---------|-------|---------|-----------|
| English US | en_US-ljspeech-high | High | ~63 MB |
| English GB | en_GB-alba-medium | Medium | ~15 MB |
| German | de_DE-thorsten-high | High | ~63 MB |
| French | fr_FR-siwis-medium | Medium | ~15 MB |
| Italian | it_IT-paola-medium | Medium | ~15 MB |
| Russian | ru_RU-irina-medium | Medium | ~15 MB |
| Turkish | tr_TR-dfki-medium | Medium | ~15 MB |
| Chinese | vits-melo-tts-zh_en (MeloTTS) | High | ~50 MB |
| Spanish | es_ES-davefx-medium | Medium | ~63 MB |
| **Total** | | | **~231 MB** |

> **GitHub Note:** GitHub enforces a 100 MB per-file limit. The two high-quality files (en_US-ljspeech-high at ~63 MB and de_DE-thorsten-high at ~63 MB) should fit. However, if they exceed 50 MB you will receive a warning. Use **GitHub Releases** as an alternative for large binary files — your app can download from the release asset URL at first launch.

---

*See `download_voices.py` to automatically download all selected models.*
