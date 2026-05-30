import { motion } from "framer-motion";

export default function WipeAnimation() {
  return (
    <motion.div
      className="wipe-banner"
      initial={{
        opacity: 0,
        scale: 0.8,
      }}
      animate={{
        opacity: 1,
        scale: 1,
      }}
      transition={{
        duration: 0.5,
      }}
    >
      MEMORY ZEROED
    </motion.div>
  );
}