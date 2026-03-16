// scripts/sync-settings.ts
// video-settings.yaml → src/config.ts に自動変換
// create-yukkuri-channel の sync-settings.ts に準拠

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';

const YAML_PATH   = path.resolve(__dirname, '../video-settings.yaml');
const CONFIG_PATH = path.resolve(__dirname, '../src/config.ts');

function toTs(obj: unknown, indent = 2): string {
  if (typeof obj === 'string') return `'${obj}'`;
  if (typeof obj === 'number' || typeof obj === 'boolean') return String(obj);
  if (Array.isArray(obj)) return `[${obj.map((v) => toTs(v)).join(', ')}]`;
  if (obj && typeof obj === 'object') {
    const pad = ' '.repeat(indent);
    const inner = Object.entries(obj as Record<string, unknown>)
      .map(([k, v]) => `${pad}${k}: ${toTs(v, indent + 2)},`)
      .join('\n');
    return `{\n${inner}\n${' '.repeat(indent - 2)}}`;
  }
  return String(obj);
}

function main() {
  const raw = fs.readFileSync(YAML_PATH, 'utf8');
  const settings = yaml.load(raw) as Record<string, unknown>;

  const tsContent = `// src/config.ts
// ⚠️ このファイルは scripts/sync-settings.ts が自動生成します
// video-settings.yaml を変更したら npm run sync-settings を実行してください

export const config = ${toTs(settings)} as const;

export type Config = typeof config;
`;

  fs.writeFileSync(CONFIG_PATH, tsContent);
  console.log('✅ src/config.ts updated from video-settings.yaml');
}

main();
