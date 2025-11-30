import { useState } from "react";

export default function PrelabelDemo({token}) {
  const [img, setImg] = useState(null);
  const [boxes, setBoxes] = useState([]);

  async function handleUpload(e) {
    const file = e.target.files[0];
    setImg(URL.createObjectURL(file));
    const form = new FormData();
    form.append("file", file);
    const res = await fetch('/api/v1/ai/prelabel', { method: 'POST', headers: {'Authorization': 'Bearer '+token}, body: form });
    if (res.ok) {
      const j = await res.json();
      setBoxes((j.prelabel && j.prelabel.boxes) || []);
    } else {
      alert('Prelabel failed');
    }
  }

  return (
    <div style={{padding:20}}>
      <h3>AI Prelabel Demo</h3>
      <input type="file" onChange={handleUpload}/>
      {img && (
        <div style={{position:'relative', display:'inline-block', marginTop:12}}>
          <img src={img} alt="preview" style={{maxWidth:400}}/>
          {boxes.map((b,i)=>(
            <div key={i} style={{
              position:'absolute', left:b.bbox[0], top:b.bbox[1], width:b.bbox[2]-b.bbox[0],
              height:b.bbox[3]-b.bbox[1], border:'2px dashed red', pointerEvents:'none'
            }} />
          ))}
        </div>
      )}
    </div>
  );
}
