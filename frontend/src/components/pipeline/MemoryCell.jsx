import { useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

import HexDump from "./HexDump";
import WipeAnimation from "../animations/WipeAnimation";

function generateBytes() {
  return Array.from(
    { length: 16 },
    () =>
      Math.floor(Math.random() * 256)
        .toString(16)
        .padStart(2, "0")
        .toUpperCase()
  );
}

export default function MemoryCell({
  title,
  state,
}) {

  const [showPopup, setShowPopup] =
    useState(true);

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
    <>
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
              <WipeAnimation />
            )}
          </>
        )}
      </motion.div>

      <AnimatePresence>
        {isWipe &&
          isDone &&
          showPopup && (

            <motion.div
              className="wipe-popup"
              initial={{
                opacity: 0,
                scale: 0.8,
              }}
              animate={{
                opacity: 1,
                scale: 1,
              }}
              exit={{
                opacity: 0,
                scale: 0.8,
              }}
            >

              <button
                className="wipe-close"
                onClick={() =>
                  setShowPopup(false)
                }
              >
                ✕
              </button>

              <h2>
                MEMORY ZEROED
              </h2>

              <p>
                All biometric traces
                have been permanently
                removed from memory.
              </p>

              <div className="wipe-bytes">
                00 00 00 00 00 00 00 00
              </div>

              <div className="wipe-status">
                [ZEROED — 256 BYTES]
              </div>

            </motion.div>
          )}
      </AnimatePresence>

      {/* Styled JSX block fixing your Vite compilation error */}
      <style>{`
        /* --- Container Layout --- */
        

       


        .waiting { color: #64748b; }
        .processing { color: #f59e0b; }

        /* --- Glassmorphism Center Popup --- */
        .wipe-popup {
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%) !important; /* Force center regardless of framer animations */
          z-index: 9999;
          width: 90%;
          max-width: 420px;
          padding: 36px 24px 28px 24px;
          box-sizing: border-box;

          /* Perfect Premium Glass Look */
          background: rgba(15, 23, 42, 0.95); 
          backdrop-filter: blur(20px) saturate(180%);
          -webkit-backdrop-filter: blur(20px) saturate(180%);
          border: 1px solid rgba(255, 255, 255, 0.12);
          border-radius: 16px;
          
          box-shadow: 
            0 25px 50px -12px rgba(0, 0, 0, 0.94),
            0 0 40px rgba(16, 185, 129, 0.74);
          
          text-align: center;
          color: #ffffff;
          font-family: system-ui, -apple-system, sans-serif;
        }

        /* Fixed Top-Right Cross Positioning */
        .wipe-close {
          position: absolute;
          top: 16px;
          right: 16px;
          background: transparent;
          border: none;
          color: rgba(255, 255, 255, 0.4);
          font-size: 1.1rem;
          cursor: pointer;
          width: 28px;
          height: 28px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 50%;
          transition: background 0.2s ease, color 0.2s ease;
        }

        .wipe-close:hover {
          background: rgba(255, 255, 255, 0.08);
          color: #ef4444;
        }

        .wipe-popup h2 {
          font-family: 'Courier New', Courier, monospace;
          font-size: 1.4rem;
          letter-spacing: 3px;
          color: #10b981;
          margin: 0 0 12px 0;
          font-weight: 700;
        }

        .wipe-popup p {
          color: #94a3b8;
          font-size: 0.95rem;
          line-height: 1.5;
          margin: 0 0 24px 0;
        }

        .wipe-bytes {
          background: rgba(0, 0, 0, 0.35);
          border: 1px dashed rgba(16, 185, 129, 0.3);
          padding: 14px;
          border-radius: 8px;
          font-family: 'Courier New', Courier, monospace;
          font-weight: 700;
          color: #34d399;
          letter-spacing: 1px;
          margin-bottom: 16px;
        }

        .wipe-status {
          font-family: 'Courier New', Courier, monospace;
          font-size: 0.75rem;
          color: rgba(255, 255, 255, 0.35);
          letter-spacing: 1px;
        }
      `}</style>
    </>
  );
}