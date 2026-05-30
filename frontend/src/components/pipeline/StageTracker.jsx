import MemoryCell from "./MemoryCell";

export default function StageTracker() {
  return (
    <div className="pipeline-grid">

      <MemoryCell
        title="CAPTURE"
        state="done"
      />

      <MemoryCell
        title="PREPROCESS"
        state="done"
      />

      <MemoryCell
        title="ERROR-CORRECT"
        state="done"
      />

      <MemoryCell
        title="HASH"
        state="done"
      />

      <MemoryCell
        title="WIPE"
        state="done"
      />

    </div>
  );
}