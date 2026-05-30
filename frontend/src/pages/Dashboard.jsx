import { useState } from "react";
import { motion } from "framer-motion";

import StageTracker from "../components/pipeline/StageTracker";
import NodeVotes from "../components/nodes/NodeVotes";
import JudgeNarrative from "../components/sidebar/JudgeNarrative";

export default function Dashboard() {

  const [darkMode, setDarkMode] = useState(true);

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
  <div
    className={`dashboard ${
      darkMode ? "theme-dark" : "theme-light"
    }`}
  >
    <div className="background-glow" />

    <div className="theme-toggle-container">
      <button
        className="theme-toggle"
        onClick={() => setDarkMode(!darkMode)}
      >
        {darkMode ? "☀ Light" : "🌙 Dark"}
      </button>
    </div>

    <header className="hero">

      <motion.h1
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        ZERO KNOWLEDGE
        <span> BIOMETRICS</span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        Privacy Preserving Identity Verification
      </motion.p>

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
          currentStage={currentStage}
        />

      </section>

    </div>

  </div>
);
}