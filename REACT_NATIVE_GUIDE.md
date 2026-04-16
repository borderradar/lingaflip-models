# React Native TTS Integration Guide
### LingaFlip — On-device voice with Piper + Kokoro

---

## Architecture Overview

```
GitHub Repo (borderradar/lingaflip-models)
  └── voices/
       ├── en_US/ljspeech/*.onnx + *.onnx.json
       ├── de_DE/thorsten/*.onnx + *.onnx.json
       └── ...

     ↓ App downloads on first use (per language)

React Native App
  └── DocumentDirectory/voices/
       └── (cached ONNX files)
            ↓
       react-native-sherpa-onnx
            ↓
       On-device audio output
```

---

## Step 1 — Install the TTS Library

The recommended library is **react-native-sherpa-onnx**. It supports Piper VITS models on both Android and iOS completely offline.

```bash
npm install react-native-sherpa-onnx
# or
yarn add react-native-sherpa-onnx
```

GitHub: https://github.com/XDcobra/react-native-sherpa-onnx

For iOS, run:
```bash
cd ios && pod install
```

---

## Step 2 — Download Models at Runtime

Models are downloaded from GitHub on first use and cached locally. Here is a reusable download utility:

```typescript
// src/tts/VoiceDownloader.ts
import * as FileSystem from 'expo-file-system'; // or react-native-fs

const GITHUB_RAW_BASE =
  'https://raw.githubusercontent.com/borderradar/lingaflip-models/main/voices';

const VOICES_MANIFEST =
  'https://raw.githubusercontent.com/borderradar/lingaflip-models/main/voices-manifest.json';

export interface VoiceEntry {
  id: string;
  locale: string;
  engine: 'piper' | 'kokoro';
  files: {
    model: string;
    config?: string;
  };
}

/** Download a voice model if not already cached */
export async function ensureVoiceDownloaded(voice: VoiceEntry): Promise<{
  modelPath: string;
  configPath?: string;
}> {
  const voiceDir = `${FileSystem.documentDirectory}voices/${voice.locale}/`;
  const modelFileName = voice.files.model.split('/').pop()!;
  const modelPath = voiceDir + modelFileName;

  // Check if already cached
  const info = await FileSystem.getInfoAsync(modelPath);
  if (!info.exists) {
    console.log(`Downloading voice model: ${voice.id}`);
    await FileSystem.makeDirectoryAsync(voiceDir, { intermediates: true });

    await FileSystem.downloadAsync(
      `${GITHUB_RAW_BASE}/${voice.files.model}`,
      modelPath
    );
  }

  let configPath: string | undefined;
  if (voice.files.config) {
    const configFileName = voice.files.config.split('/').pop()!;
    configPath = voiceDir + configFileName;
    const configInfo = await FileSystem.getInfoAsync(configPath);
    if (!configInfo.exists) {
      await FileSystem.downloadAsync(
        `${GITHUB_RAW_BASE}/${voice.files.config}`,
        configPath
      );
    }
  }

  return { modelPath, configPath };
}

/** Load the voices manifest from GitHub */
export async function loadVoicesManifest() {
  const res = await fetch(VOICES_MANIFEST);
  return res.json();
}
```

---

## Step 3 — Piper TTS (All languages except Japanese)

```typescript
// src/tts/PiperTTS.ts
import { SherpaTTS } from 'react-native-sherpa-onnx';

let ttsEngine: SherpaTTS | null = null;
let currentLocale: string | null = null;

export async function initPiperTTS(modelPath: string, configPath: string, locale: string) {
  if (currentLocale === locale && ttsEngine) return; // already loaded

  ttsEngine = new SherpaTTS({
    modelPath,
    configPath,
    // Piper uses espeak-ng for phonemization — sherpa-onnx handles this automatically
  });

  currentLocale = locale;
  console.log(`Piper TTS initialized for locale: ${locale}`);
}

export async function speak(text: string): Promise<void> {
  if (!ttsEngine) throw new Error('TTS not initialized');
  await ttsEngine.speak(text);
}

export function stopSpeaking() {
  ttsEngine?.stop();
}
```

---

## Step 4 — Japanese TTS with Kokoro

Japanese uses Kokoro TTS, which has a slightly different setup:

```typescript
// src/tts/KokoroTTS.ts
// Kokoro uses the same ONNX runtime but different voice selection

import { SherpaTTS } from 'react-native-sherpa-onnx';

let kokoroEngine: SherpaTTS | null = null;

export async function initKokoroTTS(modelPath: string) {
  kokoroEngine = new SherpaTTS({
    modelPath,
    voiceId: 'jf_alpha', // Japanese Female (alpha quality)
    // Kokoro supports multiple voices in one model:
    // 'jf_alpha' = Japanese Female (natural)
    // See: https://huggingface.co/hexgrad/Kokoro-82M for full list
  });
}

export async function speakJapanese(text: string): Promise<void> {
  if (!kokoroEngine) throw new Error('Kokoro TTS not initialized');
  await kokoroEngine.speak(text);
}
```

---

## Step 5 — Unified TTS Manager

Use a single manager that automatically selects the right engine and voice for the user's current learning language:

```typescript
// src/tts/TTSManager.ts
import { loadVoicesManifest, ensureVoiceDownloaded } from './VoiceDownloader';
import { initPiperTTS, speak as piperSpeak } from './PiperTTS';
import { initKokoroTTS, speakJapanese } from './KokoroTTS';

// Map from app language code to voice locale
const LANGUAGE_LOCALE_MAP: Record<string, string> = {
  'english-us': 'en-US',
  'english-uk': 'en-GB',
  'german':     'de-DE',
  'french':     'fr-FR',
  'italian':    'it-IT',
  'russian':    'ru-RU',
  'turkish':    'tr-TR',
  'chinese':    'zh-CN',
  'japanese':   'ja-JP',
  'spanish':    'es-MX',
};

export class TTSManager {
  private manifest: any = null;
  private loadedLocale: string | null = null;

  async initialize() {
    this.manifest = await loadVoicesManifest();
  }

  async loadLanguage(appLanguage: string) {
    const locale = LANGUAGE_LOCALE_MAP[appLanguage];
    if (!locale) throw new Error(`No voice for language: ${appLanguage}`);
    if (locale === this.loadedLocale) return; // already loaded

    const voiceEntry = this.manifest.voices.find((v: any) => v.locale === locale);
    if (!voiceEntry) throw new Error(`Voice not found in manifest: ${locale}`);

    const { modelPath, configPath } = await ensureVoiceDownloaded(voiceEntry);

    if (voiceEntry.engine === 'kokoro') {
      await initKokoroTTS(modelPath);
    } else {
      await initPiperTTS(modelPath, configPath!, locale);
    }

    this.loadedLocale = locale;
  }

  async speak(text: string, language: string) {
    await this.loadLanguage(language);
    const locale = LANGUAGE_LOCALE_MAP[language];

    if (locale === 'ja-JP') {
      const { speakJapanese } = await import('./KokoroTTS');
      await speakJapanese(text);
    } else {
      await piperSpeak(text);
    }
  }
}

// Singleton export
export const tts = new TTSManager();
```

---

## Step 6 — Usage in a Screen

```typescript
// In any React Native component:
import { tts } from '../tts/TTSManager';
import { useEffect } from 'react';

function LessonScreen({ language }: { language: string }) {

  useEffect(() => {
    tts.initialize().catch(console.error);
  }, []);

  const handlePronounce = async (word: string) => {
    try {
      await tts.speak(word, language);
    } catch (e) {
      console.error('TTS error:', e);
    }
  };

  return (
    // ... your lesson UI
  );
}
```

---

## GitHub Hosting Notes

### File URL format for your app:
```
https://raw.githubusercontent.com/borderradar/lingaflip-models/main/voices/{lang}/{voice}/{filename}
```

### Example:
```
https://raw.githubusercontent.com/borderradar/lingaflip-models/main/voices/de_DE/thorsten/de_DE-thorsten-high.onnx
```

### File size limits:
- GitHub enforces a **100 MB hard limit** per file
- Files over **50 MB** generate a warning during push
- The two high-quality models (en_US-ljspeech-high, de_DE-thorsten-high) are ~63 MB each — within limits
- If you need to go above 100 MB, use **GitHub Releases** (up to 2 GB per asset):

```bash
gh release create v1.0.0 --title "Voice Models v1.0.0"
gh release upload v1.0.0 voices/de_DE/thorsten/de_DE-thorsten-high.onnx
```

Then update the URL in your downloader to point to the release asset URL.

---

## Testing Tip

Use the Sherpa-ONNX sample app to verify your downloaded models play correctly before integrating into LingaFlip:
- https://k2-fsa.github.io/sherpa/onnx/tts/apk-engine.html (Android APK tester)

---

## Attribution (Required in App)

Add to your **About / Credits** screen or release notes:

```
TTS Voices:
• Russian: Irina voice, © RHVoice (https://github.com/RHVoice/RHVoice), CC-BY-SA 4.0
• Japanese: Kokoro-82M (hexgrad/Kokoro-82M), Apache 2.0

Piper TTS engine: https://github.com/rhasspy/piper (MIT License)
```
