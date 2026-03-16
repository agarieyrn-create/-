// editor/src/App.tsx
// GUIエディター フロントエンド（React + Vite）
// localhost:3001 で起動、localhost:3002 の REST API と通信

import React, { useEffect, useState } from 'react';

const API = 'http://localhost:3002';

interface ScriptLine {
  id: number;
  character: string;
  text: string;
  displayText?: string;
  emotion?: string;
  durationInFrames: number;
  pauseAfter: number;
}

function App() {
  const [lines, setLines] = useState<ScriptLine[]>([]);
  const [editId, setEditId] = useState<number | null>(null);
  const [editText, setEditText] = useState('');
  const [editEmotion, setEditEmotion] = useState('normal');
  const [status, setStatus] = useState('');

  const fetchScript = async () => {
    const res = await fetch(`${API}/api/script`);
    setLines(await res.json());
  };

  useEffect(() => { fetchScript(); }, []);

  const handleEdit = (line: ScriptLine) => {
    setEditId(line.id);
    setEditText(line.text);
    setEditEmotion(line.emotion ?? 'normal');
  };

  const handleSave = async () => {
    if (editId === null) return;
    await fetch(`${API}/api/script/${editId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: editText, emotion: editEmotion }),
    });
    setEditId(null);
    setStatus(`✓ ID ${editId} 更新`);
    fetchScript();
  };

  const handleAction = async (action: string) => {
    setStatus(`▶ ${action} 実行中...`);
    const res = await fetch(`${API}/api/actions/${action}`, { method: 'POST' });
    const data = await res.json();
    setStatus(data.ok ? `✓ ${action} 完了` : `✗ ${data.error}`);
  };

  return (
    <div style={{ fontFamily: 'sans-serif', padding: 24, maxWidth: 900 }}>
      <h1 style={{ color: '#FF6B9D' }}>ももちゃんとポポ — GUIエディター</h1>

      <div style={{ marginBottom: 16, display: 'flex', gap: 8 }}>
        <button onClick={() => handleAction('generate-voices')}
                style={{ padding: '8px 16px', background: '#FF8C00', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer' }}>
          音声生成
        </button>
        <button onClick={() => handleAction('build-video')}
                style={{ padding: '8px 16px', background: '#4FC3F7', color: '#fff', border: 'none', borderRadius: 6, cursor: 'pointer' }}>
          動画ビルド
        </button>
        <span style={{ alignSelf: 'center', color: '#666' }}>{status}</span>
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
        <thead>
          <tr style={{ background: '#FFF9E6' }}>
            {['ID', 'キャラ', 'セリフ', '表情', 'フレーム', '操作'].map(h => (
              <th key={h} style={{ padding: '8px 12px', textAlign: 'left', borderBottom: '2px solid #FFB3C6' }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {lines.map(line => (
            <tr key={line.id} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: '8px 12px', color: '#999' }}>{line.id}</td>
              <td style={{ padding: '8px 12px', fontWeight: 'bold',
                           color: line.character === 'momo' ? '#FF6B9D' : line.character === 'popo' ? '#FF8C00' : '#4FC3F7' }}>
                {line.character}
              </td>
              <td style={{ padding: '8px 12px', maxWidth: 300 }}>
                {editId === line.id ? (
                  <textarea
                    value={editText}
                    onChange={e => setEditText(e.target.value)}
                    style={{ width: '100%', fontSize: 13, padding: 4 }}
                    rows={2}
                  />
                ) : line.text}
              </td>
              <td style={{ padding: '8px 12px' }}>
                {editId === line.id ? (
                  <select value={editEmotion} onChange={e => setEditEmotion(e.target.value)}>
                    {['normal','happy','surprise','think','question'].map(e =>
                      <option key={e} value={e}>{e}</option>)}
                  </select>
                ) : line.emotion ?? 'normal'}
              </td>
              <td style={{ padding: '8px 12px', color: '#999' }}>{line.durationInFrames}f</td>
              <td style={{ padding: '8px 12px' }}>
                {editId === line.id ? (
                  <button onClick={handleSave}
                          style={{ padding: '4px 10px', background: '#4CAF50', color: '#fff', border: 'none', borderRadius: 4, cursor: 'pointer' }}>
                    保存
                  </button>
                ) : (
                  <button onClick={() => handleEdit(line)}
                          style={{ padding: '4px 10px', background: '#eee', border: 'none', borderRadius: 4, cursor: 'pointer' }}>
                    編集
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
