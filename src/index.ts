// src/index.ts — Remotion エントリポイント
import { registerRoot } from 'remotion';
import { Main, totalFrames } from './Main';
import { config } from './config';
import { Composition } from 'remotion';
import React from 'react';

registerRoot(() => (
  React.createElement(Composition, {
    id: 'Main',
    component: Main,
    durationInFrames: totalFrames,
    fps: config.video.fps,
    width: config.video.width,
    height: config.video.height,
  })
));
