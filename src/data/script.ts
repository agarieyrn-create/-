// src/data/script.ts
// create-yukkuri-channel ScriptLine スキーマ準拠 + v2.2 拡張フィールド

export type CharacterId = 'momo' | 'popo' | 'toto';
export type Emotion = 'normal' | 'happy' | 'surprise' | 'think' | 'question';
export type BgmType = 'upbeat' | 'calm' | 'quiz' | 'ending' | 'none';
export type VisualAnimation = 'none' | 'fadeIn' | 'slideUp' | 'slideLeft' | 'zoomIn' | 'bounce';

export interface ScriptLine {
  // ── create-yukkuri-channel 準拠フィールド ──────────────────────
  id:               number;
  character:        CharacterId;
  text:             string;               // 音声生成用（カタカナ推奨）
  displayText?:     string;               // 字幕用（英語表記など）
  scene:            number;
  voiceFile:        string;               // 例: '01_momo.wav'
  durationInFrames: number;               // 音声秒数 × 30fps × 1.2
  pauseAfter:       number;               // セリフ後の間（フレーム数）
  emotion?:         Emotion;
  // ── visual（画像・テキスト・Bロール）────────────────────────────
  visual?: {
    type:       'image' | 'text' | 'broll' | 'gif';
    src?:       string;
    text?:      string;
    fontSize?:  number;
    color?:     string;
    animation?: VisualAnimation;
  };
  // ── 効果音 ──────────────────────────────────────────────────────
  se?: {
    src:     string;  // public/se/
    volume?: number;  // 0.0 〜 1.0
  };
  // ── v2.2 拡張フィールド ─────────────────────────────────────────
  b_roll_keyword?: string;  // Pixabay/Pexels 検索キーワード（英語）
  bgm_type?:       BgmType;
}

export interface BGMConfig {
  src:    string;
  volume: number;
  loop:   boolean;
}

// ── BGM設定（ファイルレベル）────────────────────────────────────
export const bgmConfig: BGMConfig = {
  src:    'background.mp3',
  volume: 0.3,
  loop:   true,
};

// ── スクリプト本体（動画①: なんでそらはあおいの？）────────────
export const scriptData: ScriptLine[] = [
  {
    id: 1, character: 'momo', scene: 1,
    text: 'みんな〜！きょうも「なんで？」しらべちゃおう！',
    voiceFile: '01_momo.wav', durationInFrames: 90, pauseAfter: 10,
    emotion: 'happy',
    bgm_type: 'upbeat',
    se: { src: 'se_woosh.mp3', volume: 0.7 },
  },
  {
    id: 2, character: 'momo', scene: 1,
    text: 'ポポ〜！そらって なんで あおいの？',
    voiceFile: '02_momo.wav', durationInFrames: 80, pauseAfter: 10,
    emotion: 'question',
    b_roll_keyword: 'blue sky children',
  },
  {
    id: 3, character: 'popo', scene: 1,
    text: 'おっ！いい「なんで？」だワン！いっしょに かんがえよう！',
    voiceFile: '03_popo.wav', durationInFrames: 100, pauseAfter: 15,
    emotion: 'happy',
    se: { src: 'se_chime.mp3', volume: 0.6 },
  },
  {
    id: 4, character: 'popo', scene: 2,
    text: 'たいようの ひかりには にじの いろが ぜんぶ はいってるんだ！',
    voiceFile: '04_popo.wav', durationInFrames: 110, pauseAfter: 15,
    emotion: 'think',
    visual: { type: 'image', src: 'sunlight_prism.png', animation: 'fadeIn' },
  },
  {
    id: 5, character: 'momo', scene: 2,
    text: 'えっ！しろい ひかりに いろが かくれてるの？しらなかった〜！',
    displayText: 'えっ！白い光に 色が隠れてるの？知らなかった〜！',
    voiceFile: '05_momo.wav', durationInFrames: 105, pauseAfter: 10,
    emotion: 'surprise',
    se: { src: 'se_sparkle.mp3', volume: 0.6 },
  },
  {
    id: 6, character: 'popo', scene: 3,
    text: 'そらの くうきが あおい ひかりだけを はじいて ちらすんだ！',
    voiceFile: '06_popo.wav', durationInFrames: 108, pauseAfter: 15,
    emotion: 'think',
    b_roll_keyword: 'sky atmosphere light scattering',
  },
  {
    id: 7, character: 'popo', scene: 3,
    text: 'ゆうやけが オレンジなのは ひかりが とおくを とおって あかい いろだけ のこるから！',
    voiceFile: '07_popo.wav', durationInFrames: 140, pauseAfter: 15,
    emotion: 'happy',
    visual: { type: 'image', src: 'sunset.png', animation: 'fadeIn' },
    bgm_type: 'calm',
  },
  {
    id: 8, character: 'momo', scene: 4,
    text: 'そっかー！ひかりって すごいんだね！',
    voiceFile: '08_momo.wav', durationInFrames: 72, pauseAfter: 10,
    emotion: 'happy',
    se: { src: 'se_sparkle.mp3', volume: 0.7 },
  },
  {
    id: 9, character: 'popo', scene: 4,
    text: 'またいっしょに「なんで？」さがそうね！だワン♪',
    voiceFile: '09_popo.wav', durationInFrames: 90, pauseAfter: 30,
    emotion: 'happy',
    bgm_type: 'ending',
  },
];
