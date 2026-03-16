// scripts/sync-script.ts
// script.ts の整合性チェック（voiceFile の存在確認、id 重複チェック等）

import * as fs from 'fs';
import * as path from 'path';

const VOICES_DIR = path.resolve(__dirname, '../public/voices');

async function main() {
  // eslint-disable-next-line @typescript-eslint/no-var-requires
  const { scriptData } = require('../src/data/script') as {
    scriptData: Array<{ id: number; voiceFile: string; durationInFrames: number }>;
  };

  const ids = scriptData.map((l) => l.id);
  const dupIds = ids.filter((id, i) => ids.indexOf(id) !== i);
  if (dupIds.length) {
    console.error(`❌ Duplicate IDs found: ${dupIds.join(', ')}`);
    process.exit(1);
  }

  let hasError = false;
  for (const line of scriptData) {
    const voicePath = path.join(VOICES_DIR, line.voiceFile);
    if (!fs.existsSync(voicePath)) {
      console.warn(`  ⚠ Voice file missing: ${line.voiceFile} (id=${line.id})`);
      hasError = true;
    }
    if (line.durationInFrames <= 0) {
      console.warn(`  ⚠ durationInFrames <= 0: id=${line.id}`);
      hasError = true;
    }
  }

  if (hasError) {
    console.log('\n⚠ Some issues found. Run: npm run voices');
  } else {
    console.log(`✅ script.ts OK — ${scriptData.length} lines, no issues`);
  }
}

main().catch(console.error);
