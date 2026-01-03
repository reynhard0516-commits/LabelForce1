import { useRef, useState } from "react";

export default function ImageAnnotator({ imageUrl, labels, onSave }) {
  const imgRef = useRef();
  const [start, setStart] = useState(null);
  const [box, setBox] = useState(null);
  const [labelId, setLabelId] = useState("");

  function mouseDown(e) {
    const rect = imgRef.current.getBoundingClientRect();
    setStart({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  }

  function mouseMove(e) {
    if (!start) return;
    const rect = imgRef.current.getBoundingClientRect();
    setBox({
      x: start.x,
      y: start.y,
      w: e.clientX - rect.left - start.x,
      h: e.clientY - rect.top - start.y,
    });
  }

  function mouseUp() {
    setStart(null);
  }

  function save() {
    if (!box || !labelId) return;
    onSave({
      label_id: labelId,
      box,
    });
    setBox(null);
  }

  return (
    <div>
      <div style={{ position: "relative", display: "inline-block" }}>
        <img
          ref={imgRef}
          src={imageUrl}
          alt=""
          onMouseDown={mouseDown}
          onMouseMove={mouseMove}
          onMouseUp={mouseUp}
          style={{ maxWidth: "400px" }}
        />

        {box && (
          <div
            style={{
              position: "absolute",
              border: "2px solid red",
              left: box.x,
              top: box.y,
              width: box.w,
              height: box.h,
            }}
          />
        )}
      </div>

      <div>
        <select value={labelId} onChange={e => setLabelId(e.target.value)}>
          <option value="">Select label</option>
          {labels.map(l => (
            <option key={l.id} value={l.id}>
              {l.name}
            </option>
          ))}
        </select>

        <button onClick={save}>Save Box</button>
      </div>
    </div>
  );
}
