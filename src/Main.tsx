// src/Main.tsx
// Remotion ルートコンポーネント

import React from 'react';
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { scriptData, bgmConfig, ScriptLine } from './data/script';
import { Character } from './components/Character';
import { Subtitle } from './components/Subtitle';
import { SceneVisuals } from './components/SceneVisuals';
import { BGMLayer } from './components/BGMLayer';
import { config } from './config';

/** フレームオフセットからアクティブな ScriptLine を探す */
const getActiveLineAt = (frame: number): { line: ScriptLine; localFrame: number } | null => {
  let offset = 0;
  for (const line of scriptData) {
    const end = offset + line.durationInFrames + line.pauseAfter;
    if (frame >= offset && frame < end) {
      return { line, localFrame: frame - offset };
    }
    offset = end;
  }
  return null;
};

/** 全スクリプトの総フレーム数 */
export const totalFrames = scriptData.reduce(
  (sum, line) => sum + line.durationInFrames + line.pauseAfter,
  0,
);

export const Main: React.FC = () => {
  const frame = useCurrentFrame();
  const active = getActiveLineAt(frame);

  if (!active) return null;

  const { line, localFrame } = active;
  const isSpeaking = localFrame < line.durationInFrames;

  return (
    <AbsoluteFill style={{ backgroundColor: config.colors.background }}>

      {/* ── ビジュアルレイヤー（背景・Bロール・画像） */}
      <SceneVisuals visual={line.visual} />

      {/* ── キャラクター */}
      <AbsoluteFill
        style={{
          display: 'flex',
          alignItems: 'flex-end',
          justifyContent: 'center',
          paddingBottom: config.subtitle.containerHeight + 20,
        }}
      >
        <Character
          characterId={line.character}
          emotion={line.emotion}
          isSpeaking={isSpeaking}
        />
      </AbsoluteFill>

      {/* ── 字幕 */}
      <Subtitle
        text={line.text}
        displayText={line.displayText}
        characterId={line.character}
      />

      {/* ── BGM / SE */}
      <BGMLayer bgmConfig={bgmConfig} se={line.se} />

    </AbsoluteFill>
  );
};
