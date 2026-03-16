// src/components/Subtitle.tsx
// displayText（字幕用）/ text（音声用）の2フィールド分離に対応

import React from 'react';
import { CharacterId } from '../data/script';
import { config } from '../config';

interface SubtitleProps {
  text: string;          // 音声用テキスト（カタカナ）
  displayText?: string;  // 字幕用テキスト（英語・漢字表記など）
  characterId: CharacterId;
}

export const Subtitle: React.FC<SubtitleProps> = ({
  text,
  displayText,
  characterId,
}) => {
  // 表示するテキスト: displayText が設定されていればそちらを優先
  const shownText = displayText ?? text;
  const speakerStyle = config.subtitle.speakers[characterId];

  return (
    <div
      style={{
        position: 'absolute',
        bottom: config.subtitle.bottomOffset,
        left: 0,
        right: 0,
        height: config.subtitle.containerHeight,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: `0 ${(100 - config.subtitle.maxWidthPercent) / 2}%`,
      }}
    >
      <span
        style={{
          fontFamily: config.font.family,
          fontSize: config.font.size,
          fontWeight: config.font.weight,
          color: speakerStyle.fillColor,
          // アウトライン（外側・内側の2重）
          textShadow: [
            // 外側（黒）
            ...Array.from({ length: 8 }, (_, i) => {
              const angle = (i * Math.PI) / 4;
              const w = config.subtitle.outerOutlineWidth;
              return `${Math.cos(angle) * w}px ${Math.sin(angle) * w}px 0 ${speakerStyle.outerOutlineColor}`;
            }),
            // 内側（白）
            ...Array.from({ length: 8 }, (_, i) => {
              const angle = (i * Math.PI) / 4;
              const w = config.subtitle.innerOutlineWidth;
              return `${Math.cos(angle) * w}px ${Math.sin(angle) * w}px 0 ${speakerStyle.innerOutlineColor}`;
            }),
          ].join(', '),
          lineHeight: 1.4,
          textAlign: 'center',
          whiteSpace: 'pre-wrap',
        }}
      >
        {shownText}
      </span>
    </div>
  );
};
