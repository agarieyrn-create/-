// src/components/Character.tsx
// 口パク（mouth_open/close）＋表情切り替えコンポーネント
// create-yukkuri-channel の命名規則に準拠

import React from 'react';
import { useCurrentFrame, staticFile } from 'remotion';
import { CharacterId, Emotion } from '../data/script';
import { config } from '../config';

interface CharacterProps {
  characterId: CharacterId;
  emotion?: Emotion;
  isSpeaking: boolean;    // 発声中か否か（口パクON/OFF）
  mouthOpenInterval?: number; // 口開閉の間隔（フレーム数、デフォルト4）
}

/** emotion → ファイル名プレフィックスの変換 */
const emotionToPrefix = (emotion: Emotion = 'normal'): string => {
  const map: Record<Emotion, string> = {
    normal:   'mouth',
    happy:    'happy',
    surprise: 'surprise',
    think:    'thinking',
    question: 'question',
  };
  return map[emotion];
};

/** 画像パスを解決する。存在しない表情は mouth にフォールバック */
const resolveImagePath = (
  characterId: CharacterId,
  emotion: Emotion = 'normal',
  mouthState: 'open' | 'close'
): string => {
  const base = `${config.character.imagesBasePath}/${characterId}`;
  const prefix = emotionToPrefix(emotion);
  return staticFile(`${base}/${prefix}_${mouthState}.png`);
};

export const Character: React.FC<CharacterProps> = ({
  characterId,
  emotion = 'normal',
  isSpeaking,
  mouthOpenInterval = 4,
}) => {
  const frame = useCurrentFrame();

  // 口パク: isSpeaking 中は mouthOpenInterval フレームごとに open/close を切り替え
  const mouthState: 'open' | 'close' =
    isSpeaking && Math.floor(frame / mouthOpenInterval) % 2 === 0
      ? 'open'
      : 'close';

  const imgSrc = resolveImagePath(characterId, emotion, mouthState);

  return (
    <img
      src={imgSrc}
      alt={characterId}
      style={{
        height: config.character.height,
        objectFit: 'contain',
        // 表情差分がない場合は onError でフォールバック（mouth_open/close）
      }}
      onError={(e) => {
        const target = e.currentTarget;
        const fallbackSrc = resolveImagePath(characterId, 'normal', mouthState);
        if (target.src !== fallbackSrc) {
          target.src = fallbackSrc;
        }
      }}
    />
  );
};
