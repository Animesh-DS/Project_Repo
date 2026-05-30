import { motion } from "framer-motion";

export default function HexDump({
  bytes,
  wipe = false,
}) {
  return (
    <div className="hex-grid">
      {bytes.map((byte, index) => (
        <motion.div
          key={index}
          className="hex-item"
          animate={{
            color: wipe
              ? "#ff4040"
              : "#00ff99",
          }}
          transition={{
            delay: index * 0.05,
          }}
        >
          <span className="address">
            0x00{(160 + index)
              .toString(16)
              .toUpperCase()}
          </span>

          <span className="value">
            {wipe ? "00" : byte}
          </span>
        </motion.div>
      ))}
    </div>
  );
}