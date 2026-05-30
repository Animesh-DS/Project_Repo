import { motion } from "framer-motion";
import MemoryCell from "./MemoryCell";

export default function StageTracker({
  stageStates,
}) {
  return (
    <div className="pipeline-grid">
      <MemoryCell
        title="CAPTURE"
        state={stageStates.capture}
      />

      <MemoryCell
        title="PREPROCESS"
        state={stageStates.preprocess}
      />

      <MemoryCell
        title="ERROR-CORRECT"
        state={stageStates.error_correct}
      />

      <MemoryCell
        title="HASH"
        state={stageStates.hash}
      />

      <MemoryCell
        title="WIPE"
        state={stageStates.wipe}
      />
    </div>
  );
}