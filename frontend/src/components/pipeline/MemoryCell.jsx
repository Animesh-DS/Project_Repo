import { useMemo } from "react";
import { motion } from "framer-motion";

import HexDump from "./HexDump";
import WipeAnimation from "../animations/WipeAnimation";

function generateBytes() {
  return Array.from(
    { length: 16 },
    () =>
      Math.floor(
        Math.random() * 256
      )
        .toString(16)
        .padStart(2, "0")
        .toUpperCase()
  );
}

export default function MemoryCell({
  title,
  state,
}) {
  const bytes = useMemo(
    () => generateBytes(),
    []
  );

  const isRunning =
    state === "running";

  const isDone =
    state === "done";

  const isWipe =
    title === "WIPE";

  return (
    <motion.div
      className={`
      memory-cell
      ${isRunning ? "running" : ""}
      ${isDone ? "done" : ""}
      `}
      animate={{
        scale:
          isRunning
            ? [1, 1.02, 1]
            : 1,
      }}
      transition={{
        duration: 1,
        repeat:
          isRunning
            ? Infinity
            : 0,
      }}
    >
      <div className="memory-title">
        {title}
      </div>

      {!isDone && !isRunning && (
        <div className="waiting">
          Waiting...
        </div>
      )}

      {isRunning && (
        <div className="processing">
          Processing...
        </div>
      )}

      {isDone && (
        <>
          <HexDump
            bytes={bytes}
            wipe={isWipe}
          />

          {isWipe && (
            <>
              <WipeAnimation />

              <div className="zeroed-text">
                [ZEROED — 256 BYTES]
              </div>
            </>
          )}
        </>
      )}
    </motion.div>
  );
}