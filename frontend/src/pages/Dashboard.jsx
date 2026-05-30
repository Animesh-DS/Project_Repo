import { useContext } from "react";
import { motion } from "framer-motion";

import StageTracker from "../components/pipeline/StageTracker";
import NodeVotes from "../components/nodes/NodeVotes";
import JudgeNarrative from "../components/sidebar/JudgeNarrative";

import {
  PipelineContext,
} from "../context/PipelineContext";

import useWebSocket from "../hooks/useWebSocket";

import {
  enrol,
  authenticate,
} from "../services/api";

export default function Dashboard() {

  /* ==========================================
     P3 FRONTEND ENTRY POINT

     This component DOES NOT control
     the authentication flow.

     It ONLY visualises events coming
     from the backend.

     Backend Owner:
     P4 (Animesh)

     Event Source:
     ws://localhost:8000/ws/pipeline
  ========================================== */

  useWebSocket();

  const {
    state,
  } = useContext(
    PipelineContext
  );

  const {
    stages,
    verifyResult,
    commitment_hex,
    verified_zero,
  } = state;

  /* ==========================================
     Disable buttons while pipeline running
  ========================================== */

  const pipelineRunning =
    Object.values(stages).includes(
      "start"
    );

  return (
    <div className="dashboard">

      {/* ======================================
         Animated Aurora Background
      ====================================== */}
      <div className="background-glow" />

      {/* ======================================
         HERO SECTION
      ====================================== */}
      <header className="hero">

        <motion.h1
          initial={{
            opacity: 0,
            y: -30,
          }}
          animate={{
            opacity: 1,
            y: 0,
          }}
          transition={{
            duration: 0.8,
          }}
        >
          ZERO KNOWLEDGE
          <span> BIOMETRICS</span>
        </motion.h1>

        <motion.p
          initial={{
            opacity: 0,
          }}
          animate={{
            opacity: 1,
          }}
          transition={{
            delay: 0.3,
          }}
        >
          Privacy Preserving Identity Verification
        </motion.p>

        {/* ==============================
           Backend Trigger Buttons

           P4 should expose:

           POST /enrol

           POST /authenticate
        ============================== */}
        <div className="action-buttons">

          <button
            className="primary-btn"
            disabled={pipelineRunning}
            onClick={enrol}
          >
            ENROL
          </button>

          <button
            className="secondary-btn"
            disabled={pipelineRunning}
            onClick={authenticate}
          >
            AUTHENTICATE
          </button>

        </div>

      </header>

      {/* ======================================
         MEMORY TRACE PANEL
      ====================================== */}
      <section className="memory-panel glass">

        <div className="section-title">
          MEMORY TRACE VISUALISER
        </div>

        {/* ==================================
           Stages are driven entirely by
           backend WebSocket events.

           Example:

           {
             stage:"capture",
             status:"start"
           }

           {
             stage:"capture",
             status:"done"
           }
        ================================== */}

        <StageTracker
          stageStates={stages}
        />

      </section>

      {/* ======================================
         HASH COMMITMENT DISPLAY

         Only show first 8 chars.

         Never expose full hash.
      ====================================== */}

      {commitment_hex && (

        <section
          className="glass commitment-panel"
        >

          <div className="section-title">
            COMMITMENT HASH
          </div>

          <div className="commitment-value">
            {commitment_hex}...
          </div>

        </section>

      )}

      {/* ======================================
         MEMORY WIPE STATUS
      ====================================== */}

      {verified_zero && (

        <section
          className="glass wipe-status-panel"
        >

          <div className="wipe-success">

            ✓ MEMORY VERIFIED AS ZEROED

          </div>

        </section>

      )}

      {/* ======================================
         LOWER PANELS
      ====================================== */}

      <div className="bottom-layout">

        {/* ==============================
           NODE CONSENSUS PANEL
        ============================== */}
        <section className="glass node-panel">

          <div className="section-title">
            DECENTRALISED VERIFICATION
          </div>

          <NodeVotes
            verifyResult={
              verifyResult
            }
          />

        </section>

        {/* ==============================
           JUDGE EXPLANATION PANEL
        ============================== */}
        <section className="glass narrative-panel">

          <div className="section-title">
            JUDGE NARRATIVE
          </div>

          <JudgeNarrative
            stages={stages}
          />

        </section>

      </div>

    </div>
  );
}