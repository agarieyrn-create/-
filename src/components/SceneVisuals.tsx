// src/components/SceneVisuals.tsx
// visual.type: image / text / broll / gif に対応
// コンテンツ全画面表示（余白ゼロ）・字幕とキャラは上に重ねる設計

import React from 'react';
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  staticFile,
  Video,
  Img,
} from 'remotion';
import { ScriptLine } from '../data/script';
import { config } from '../config';

type VisualConfig = NonNullable<ScriptLine['visual']>;

interface SceneVisualsProps {
  visual?: VisualConfig;
}

/** アニメーション → スタイル変換 */
const useAnimationStyle = (
  animation: VisualConfig['animation'] = 'none',
  frame: number,
  durationInFrames: number,
): React.CSSProperties => {
  switch (animation) {
    case 'fadeIn':
      return { opacity: interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' }) };
    case 'slideUp':
      return {
        transform: `translateY(${interpolate(frame, [0, 20], [60, 0], { extrapolateRight: 'clamp' })}px)`,
        opacity: interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' }),
      };
    case 'slideLeft':
      return {
        transform: `translateX(${interpolate(frame, [0, 20], [80, 0], { extrapolateRight: 'clamp' })}px)`,
        opacity: interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' }),
      };
    case 'zoomIn':
      return {
        transform: `scale(${interpolate(frame, [0, 20], [0.8, 1], { extrapolateRight: 'clamp' })})`,
        opacity: interpolate(frame, [0, 20], [0, 1], { extrapolateRight: 'clamp' }),
      };
    case 'bounce': {
      const bounce = Math.abs(Math.sin(frame * 0.3)) * 10;
      return { transform: `translateY(-${bounce}px)` };
    }
    default:
      return {};
  }
};

export const SceneVisuals: React.FC<SceneVisualsProps> = ({ visual }) => {
  const frame = useCurrentFrame();
  const { durationInFrames, width, height } = useVideoConfig();

  if (!visual) {
    // ビジュアルなし → 背景色のみ
    return (
      <div
        style={{
          position: 'absolute', inset: 0,
          backgroundColor: config.colors.background,
        }}
      />
    );
  }

  const animStyle = useAnimationStyle(visual.animation, frame, durationInFrames);
  const fullScreen: React.CSSProperties = {
    position: 'absolute', inset: 0,
    width: '100%', height: '100%',
    objectFit: 'cover',
  };

  switch (visual.type) {
    case 'image':
      return (
        <Img
          src={staticFile(`content/${visual.src ?? ''}`)}
          style={{ ...fullScreen, ...animStyle }}
        />
      );

    case 'broll':
      return (
        <Video
          src={staticFile(`assets/b_roll_cache/${visual.src ?? ''}`)}
          style={fullScreen}
          muted
        />
      );

    case 'gif':
      return (
        <Img
          src={staticFile(`assets/reaction_gifs/${visual.src ?? ''}`)}
          style={{ ...fullScreen, ...animStyle }}
        />
      );

    case 'text':
      return (
        <div
          style={{
            position: 'absolute', inset: 0,
            backgroundColor: config.colors.background,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <span
            style={{
              fontSize: visual.fontSize ?? 80,
              fontFamily: config.font.family,
              fontWeight: config.font.weight,
              color: visual.color ?? config.colors.text,
              textAlign: 'center',
              ...animStyle,
            }}
          >
            {visual.text}
          </span>
        </div>
      );

    default:
      return null;
  }
};
