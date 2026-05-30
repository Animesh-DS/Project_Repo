import { useState } from "react";
import { motion } from "framer-motion";

import StageTracker from "../components/pipeline/StageTracker";
import NodeVotes from "../components/nodes/NodeVotes";
import JudgeNarrative from "../components/sidebar/JudgeNarrative";

export default function Dashboard() {

  const [verified, setVerified] =
    useState(false);

  const [currentStage,
    setCurrentStage] =
    useState("");

  const [stageStates,
    setStageStates] =
    useState({
      capture: "",
      preprocess: "",
      error_correct: "",
      hash: "",
      wipe: "",
    });

  const runDemo = async () => {

    setVerified(false);

    const stages = [
      "capture",
      "preprocess",
      "error_correct",
      "hash",
      "wipe",
    ];

    const newState = {
      capture: "",
      preprocess: "",
      error_correct: "",
      hash: "",
      wipe: "",
    };

    setStageStates(newState);

    for (const stage of stages) {

      setCurrentStage(stage);

      setStageStates(prev => ({
        ...prev,
        [stage]: "running",
      }));

      await new Promise(r =>
        setTimeout(r, 1000)
      );

      setStageStates(prev => ({
        ...prev,
        [stage]: "done",
      }));

      await new Promise(r =>
        setTimeout(r, 600)
      );
    }

    setVerified(true);
  };

  return (
    <div className="dashboard">

      <div className="background-glow" />

      <header className="hero">

        <h1>
          ZERO KNOWLEDGE
          <span> BIOMETRICS</span>
        </h1>

        <p>
          Privacy Preserving Identity Verification
        </p>

        <div className="action-buttons">

          <button
            className="primary-btn"
            onClick={runDemo}
          >
            ENROL
          </button>

          <button
            className="secondary-btn"
            onClick={runDemo}
          >
            AUTHENTICATE
          </button>

        </div>

      </header>

      <section className="memory-panel glass">

        <div className="section-title">
          MEMORY TRACE VISUALISER
        </div>

        <StageTracker
          stageStates={stageStates}
        />

      </section>

      <div className="bottom-layout">

        <section className="glass node-panel">

          <div className="section-title">
            DECENTRALISED VERIFICATION
          </div>

          <NodeVotes
            verified={verified}
          />

        </section>

        <section className="glass narrative-panel">

          <div className="section-title">
            JUDGE NARRATIVE
          </div>

          <JudgeNarrative
            currentStage={
              currentStage
            }
          />

        </section>

      </div>

    </div>
  );
}