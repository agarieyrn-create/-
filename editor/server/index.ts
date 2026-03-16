// editor/server/index.ts
// GUIエディター REST API サーバー（localhost:3002）
// create-yukkuri-channel の GUIエディター設計に準拠

import express from 'express';
import cors from 'cors';
import * as fs from 'fs';
import * as path from 'path';

const app  = express();
const PORT = 3002;

const SCRIPT_PATH   = path.resolve(__dirname, '../../src/data/script.ts');
const SETTINGS_PATH = path.resolve(__dirname, '../../video-settings.yaml');
const CHAR_CONFIG   = path.resolve(__dirname, '../../config/characters.json');

app.use(cors());
app.use(express.json());

// ── ヘルパー ──────────────────────────────────────────────────────
function readScript(): unknown[] {
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  const mod = require('../../src/data/script');
  delete require.cache[require.resolve('../../src/data/script')];
  return mod.scriptData;
}

function writeScriptLine(id: number, updates: Record<string, unknown>) {
  let src = fs.readFileSync(SCRIPT_PATH, 'utf8');
  for (const [key, value] of Object.entries(updates)) {
    const val = typeof value === 'string' ? `'${value}'` : String(value);
    // id: N, ..., key: OLD → key: NEW
    src = src.replace(
      new RegExp(`(id: ${id},[^}]*?${key}: )[^,\\n]+`),
      `$1${val}`,
    );
  }
  fs.writeFileSync(SCRIPT_PATH, src);
}

// ── メタデータ（token節約: 最初に1回だけ叩く） ───────────────────
app.get('/api/metadata/all', (_req, res) => {
  const charCfg = JSON.parse(fs.readFileSync(CHAR_CONFIG, 'utf8'));
  res.json({
    characters:  Object.keys(charCfg.characters),
    emotions:    ['normal', 'happy', 'surprise', 'think', 'question'],
    bgmTypes:    ['upbeat', 'calm', 'quiz', 'ending', 'none'],
    animations:  ['none', 'fadeIn', 'slideUp', 'slideLeft', 'zoomIn', 'bounce'],
    visualTypes: ['image', 'text', 'broll', 'gif'],
  });
});

// ── スクリプト一覧 ────────────────────────────────────────────────
app.get('/api/script', (_req, res) => {
  res.json(readScript());
});

// ── 1行取得 ───────────────────────────────────────────────────────
app.get('/api/script/:id', (req, res) => {
  const id = Number(req.params.id);
  const line = readScript().find((l: any) => l.id === id);
  if (!line) return res.status(404).json({ error: 'Not found' });
  res.json(line);
});

// ── 1行更新（token節約・ファイル直接編集より高速） ────────────────
app.put('/api/script/:id', (req, res) => {
  const id = Number(req.params.id);
  writeScriptLine(id, req.body);
  res.json({ ok: true, id, updates: req.body });
});

// ── 1行追加 ───────────────────────────────────────────────────────
app.post('/api/script', (req, res) => {
  const lines = readScript() as any[];
  const newId = Math.max(...lines.map((l: any) => l.id)) + 1;
  const newLine = {
    id: newId,
    durationInFrames: 60,
    pauseAfter: 15,
    voiceFile: `${String(newId).padStart(2, '0')}_${req.body.character}.wav`,
    ...req.body,
  };
  // script.ts の scriptData 配列末尾に追加
  let src = fs.readFileSync(SCRIPT_PATH, 'utf8');
  const entry = JSON.stringify(newLine, null, 4)
    .replace(/"([^"]+)":/g, '$1:')   // TS形式に変換
    .replace(/"/g, "'");
  src = src.replace(/(\];\s*$)/, `  ${entry},\n$1`);
  fs.writeFileSync(SCRIPT_PATH, src);
  res.json({ ok: true, line: newLine });
});

// ── 1行削除 ───────────────────────────────────────────────────────
app.delete('/api/script/:id', (req, res) => {
  const id = Number(req.params.id);
  let src = fs.readFileSync(SCRIPT_PATH, 'utf8');
  // id: N, で始まるブロック { ... } を削除（簡易実装）
  src = src.replace(new RegExp(`\\{[^}]*?id: ${id},[^}]*?\\},?\\n`, 's'), '');
  fs.writeFileSync(SCRIPT_PATH, src);
  res.json({ ok: true, deleted: id });
});

// ── 設定取得 ─────────────────────────────────────────────────────
app.get('/api/settings', (_req, res) => {
  const raw = fs.readFileSync(SETTINGS_PATH, 'utf8');
  res.json({ yaml: raw });
});

// ── 設定更新（sync-settings を自動実行） ─────────────────────────
app.put('/api/settings', (req, res) => {
  const { yaml } = req.body as { yaml: string };
  fs.writeFileSync(SETTINGS_PATH, yaml);
  const { execSync } = require('child_process');
  try {
    execSync('npm run sync-settings', { cwd: path.resolve(__dirname, '../..') });
    res.json({ ok: true, message: 'Settings saved and synced' });
  } catch (e) {
    res.status(500).json({ error: 'sync-settings failed', detail: String(e) });
  }
});

// ── アクション ───────────────────────────────────────────────────
app.post('/api/actions/generate-voices', (_req, res) => {
  const { execSync } = require('child_process');
  try {
    execSync('npm run voices', { cwd: path.resolve(__dirname, '../..') });
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ error: String(e) });
  }
});

app.post('/api/actions/build-video', (_req, res) => {
  const { execSync } = require('child_process');
  try {
    execSync('npm run build', { cwd: path.resolve(__dirname, '../..') });
    res.json({ ok: true, output: 'out/video.mp4' });
  } catch (e) {
    res.status(500).json({ error: String(e) });
  }
});

app.listen(PORT, () => {
  console.log(`GUIエディター API: http://localhost:${PORT}`);
  console.log(`  GET  /api/metadata/all     — キャラ・感情一覧`);
  console.log(`  GET  /api/script           — スクリプト一覧`);
  console.log(`  PUT  /api/script/:id       — セリフ更新`);
  console.log(`  POST /api/actions/generate-voices  — 音声生成`);
  console.log(`  POST /api/actions/build-video      — 動画ビルド`);
});
