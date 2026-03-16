// src/config.ts
// ⚠️ このファイルは scripts/sync-settings.ts が自動生成します
// video-settings.yaml を変更したら npm run sync-settings を実行してください

export const config = {
  font: {
    family: 'Noto Sans JP',
    size: 62,
    weight: '900',
  },
  subtitle: {
    containerHeight: 216,
    bottomOffset: 0,
    maxWidthPercent: 80,
    maxWidthPixels: 1600,
    outerOutlineWidth: 20,
    outerOutlineColor: '#000000',
    innerOutlineWidth: 14,
    innerOutlineColor: '#FFFFFF',
    speakers: {
      momo: { fillColor: '#FF6B9D', innerOutlineColor: '#FFFFFF', outerOutlineColor: '#000000' },
      popo: { fillColor: '#FF8C00', innerOutlineColor: '#FFFFFF', outerOutlineColor: '#000000' },
      toto: { fillColor: '#4FC3F7', innerOutlineColor: '#FFFFFF', outerOutlineColor: '#000000' },
    },
  },
  character: {
    height: 400,
    useImages: true,
    imagesBasePath: 'images',
  },
  content: {
    topPadding: 0,
    sidePadding: 0,
    bottomPadding: 0,
  },
  video: {
    width: 1920,
    height: 1080,
    fps: 30,
    playbackRate: 1.0,
  },
  colors: {
    background: '#FFF9E6',
    text: '#2D3436',
    momo: '#FF6B9D',
    popo: '#FF8C00',
    toto: '#4FC3F7',
  },
} as const;

export type Config = typeof config;
