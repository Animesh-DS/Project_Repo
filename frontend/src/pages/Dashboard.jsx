import { motion } from "framer-motion";
import StageTracker
from "../components/pipeline/StageTracker";

export default function Dashboard() {
  return (
    <div className="dashboard">

      <div className="background-glow"></div>

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

          <button className="primary-btn">
            ENROL
          </button>

          <button className="secondary-btn">
            AUTHENTICATE
          </button>

        </div>
      </header>

      <section className="memory-panel glass">
        <div className="section-title">
          MEMORY TRACE VISUALISER
        </div>

       <StageTracker />
      </section>

      <div className="bottom-layout">

        <section className="glass node-panel">
          <div className="section-title">
            DECENTRALISED VERIFICATION
          </div>

          <div className="coming-soon">
            Node Consensus Panel
          </div>
        </section>

        <section className="glass narrative-panel">
          <div className="section-title">
            JUDGE NARRATIVE
          </div>

          <div className="coming-soon">
            Event Explanation Timeline
          </div>
        </section>

      </div>

    </div>
  );
}