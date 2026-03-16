// src/components/BGMLayer.tsx
// BGM（ループ）＋ SE（効果音）レイヤー

import React from 'react';
import { Audio, staticFile, useVideoConfig, Loop } from 'remotion';
import { BGMConfig, ScriptLine } from '../data/script';

interface BGMLayerProps {
  bgmConfig: BGMConfig;
  se?: ScriptLine['se'];
}

export const BGMLayer: React.FC<BGMLayerProps> = ({ bgmConfig, se }) => {
  const { durationInFrames } = useVideoConfig();

  return (
    <>
      {/* BGM（全編ループ） */}
      <Loop durationInFrames={durationInFrames}>
        <Audio
          src={staticFile(`bgm/${bgmConfig.src}`)}
          volume={bgmConfig.volume}
        />
      </Loop>

      {/* SE（効果音・セリフ開始と同時に1回再生） */}
      {se && (
        <Audio
          src={staticFile(`se/${se.src}`)}
          volume={se.volume ?? 0.7}
        />
      )}
    </>
  );
};
