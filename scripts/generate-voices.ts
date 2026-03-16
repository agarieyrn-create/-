// scripts/generate-voices.ts
// VOICEVOX API 経由で音声ファイルを生成し、durationInFrames を自動更新
// create-yukkuri-channel の generate-voices.ts に準拠

import * as fs from 'fs';
import * as path from 'path';
import axios from 'axios';

const VOICEVOX_URL = 'http://localhost:50021';
const VOICES_DIR   = path.resolve(__dirname, '../public/voices');
const SCRIPT_PATH  = path.resolve(__dirname, '../src/data/script.ts');
const FPS          = 30;
const PLAYBACK_RATE = 1.2;

const SPEAKER_IDS: Record<string, number> = {
  momo: 3,
  popo: 1,
  toto: 8,
};

interface ScriptLineRaw {
  id: number;
  character: string;
  text: string;
  voiceFile: string;
  durationInFrames: number;
}

async function getAudioDuration(wavBuffer: Buffer): Promise<number> {
  // WAV ヘッダからサンプル数とサンプルレートを読み取り秒数を計算
  const sampleRate  = wavBuffer.readUInt32LE(24);
  const numChannels = wavBuffer.readUInt16LE(22);
  const bitsPerSample = wavBuffer.readUInt16LE(34);
  const dataSize    = wavBuffer.readUInt32LE(40);
  return dataSize / (sampleRate * numChannels * (bitsPerSample / 8));
}

async function generateVoice(
  text: string,
  speakerId: number,
  outputPath: string,
): Promise<number> {
  // 1. audio_query
  const queryRes = await axios.post(`${VOICEVOX_URL}/audio_query`, null, {
    params: { text, speaker: speakerId },
  });
  // 2. synthesis
  const synthRes = await axios.post(
    `${VOICEVOX_URL}/synthesis`,
    queryRes.data,
    { params: { speaker: speakerId }, responseType: 'arraybuffer' },
  );
  const wavBuffer = Buffer.from(synthRes.data);
  fs.writeFileSync(outputPath, wavBuffer);
  return getAudioDuration(wavBuffer);
}

async function main() {
  if (!fs.existsSync(VOICES_DIR)) fs.mkdirSync(VOICES_DIR, { recursive: true });

  // script.ts を動的にインポート（ts-node 経由）
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  const { scriptData } = require('../src/data/script') as { scriptData: ScriptLineRaw[] };

  const updates: Record<number, number> = {}; // id → new durationInFrames

  for (const line of scriptData) {
    const speakerId = SPEAKER_IDS[line.character];
    if (!speakerId) {
      console.warn(`  ⚠ Unknown character: ${line.character} (id=${line.id})`);
      continue;
    }
    const outputPath = path.join(VOICES_DIR, line.voiceFile);
    console.log(`▶ [${line.id}] ${line.character}: "${line.text.slice(0, 20)}..."`);
    try {
      const durationSec = await generateVoice(line.text, speakerId, outputPath);
      const newFrames   = Math.ceil(durationSec * FPS * PLAYBACK_RATE);
      updates[line.id]  = newFrames;
      console.log(`  ✓ ${line.voiceFile} (${durationSec.toFixed(2)}s → ${newFrames}f)`);
    } catch (err) {
      console.error(`  ✗ Failed: ${(err as Error).message}`);
    }
  }

  // script.ts の durationInFrames を一括更新
  let src = fs.readFileSync(SCRIPT_PATH, 'utf8');
  for (const [id, frames] of Object.entries(updates)) {
    // id: N, ... durationInFrames: OLD → durationInFrames: NEW
    src = src.replace(
      new RegExp(`(id: ${id},.*?durationInFrames: )\\d+`, 's'),
      `$1${frames}`,
    );
  }
  fs.writeFileSync(SCRIPT_PATH, src);
  console.log('\n✅ durationInFrames updated in script.ts');
}

main().catch(console.error);
