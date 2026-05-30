import { motion } from "framer-motion";
import MemoryCell from "./MemoryCell";

export default function StageTracker({
  stageStates = {},
}) {

  /* ==========================================
     P3 FRONTEND

     Receives stage status from backend.

     Expected values:

     "start"
     "done"
     "error"

     Source:
     PipelineContext -> WebSocket

     P4 MUST emit:

     {
       stage:"capture",
       status:"start"
     }

  ========================================== */

  const stages = [
    {
      title: "CAPTURE",
      key: "capture",
    },
    {
      title: "PREPROCESS",
      key: "preprocess",
    },
    {
      title: "ERROR-CORRECT",
      key: "error_correct",
    },
    {
      title: "HASH",
      key: "hash",
    },
    {
      title: "WIPE",
      key: "wipe",
    },
  ];

  return (
    <div className="pipeline-grid">

      {stages.map(
        (stage, index) => (
          <div
            key={stage.key}
            className="pipeline-stage"
          >

            <MemoryCell
              title={stage.title}
              state={
                stageStates[
                  stage.key
                ] || ""
              }
            />

            {/* =========================
               Animated Connector
            ========================= */}

            {index <
              stages.length - 1 && (
              <motion.div
                className="pipeline-arrow"
                animate={{
                  opacity: [
                    0.3,
                    1,
                    0.3,
                  ],
                }}
                transition={{
                  duration: 1.5,
                  repeat:
                    Infinity,
                }}
              >
                →
              </motion.div>
            )}

          </div>
        )
      )}

    </div>
  );
}