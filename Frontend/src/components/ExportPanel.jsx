import React from 'react';
import { db } from '../db';
import JSZip from 'jszip';

function downloadFile(filename, content, mime='application/octet-stream') {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export default function ExportPanel(){
  async function exportJSON(){
    const items = await db.labels.toArray();
    downloadFile('labels_export.json', JSON.stringify(items, null, 2), 'application/json');
  }
  async function exportCSV(){
    const items = await db.labels.toArray();
    const rows = items.map(it => ({id: it.id, fileName: it.fileName, labels: JSON.stringify(it.labels)}));
    const keys = Object.keys(rows[0] || {});
    const lines = [keys.join(',')].concat(rows.map(r=>keys.map(k=>`"${String(r[k]||'').replace(/"/g,'""')}"`).join(',')));
    downloadFile('labels_export.csv', lines.join('\\n'), 'text/csv');
  }
  async function exportYOLO(){
    const items = await db.labels.toArray();
    const zip = new JSZip();
    for (const it of items){
      const name = it.fileName.replace(/\.[^/.]+$/,'');
      zip.file(name+'.txt', (it.labels||[]).map(l=> (l.class||l.label||0) + ' 0 0 0 0').join('\\n'));
    }
    const blob = await zip.generateAsync({type:'blob'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'yolo_labels.zip';
    a.click();
  }
  return (<div style={{padding:20}}>
    <h3>Export</h3>
    <button onClick={exportJSON}>Export JSON</button>
    <button onClick={exportCSV} style={{marginLeft:8}}>Export CSV</button>
    <button onClick={exportYOLO} style={{marginLeft:8}}>Export YOLO</button>
  </div>);
}
