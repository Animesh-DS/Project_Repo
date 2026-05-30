import { motion } from "framer-motion";

export default function NodeVotes({
  verified,
}) {
  const nodes = verified
    ? [true, true, true]
    : [null, null, null];

  return (
    <>
      <div className="node-grid">

        {nodes.map((node, index) => (
          <motion.div
            key={index}
            className={`
            node-card
            ${
              node === true
                ? "success"
                : ""
            }
            `}
          >
            <h3>
              Node {index + 1}
            </h3>

            <div className="vote">
              {node === true
                ? "✓"
                : "⟳"}
            </div>
          </motion.div>
        ))}

      </div>

      {verified && (
        <motion.div
          className="verdict"
          initial={{
            opacity: 0,
          }}
          animate={{
            opacity: 1,
          }}
        >
          IDENTITY VERIFIED
        </motion.div>
      )}
    </>
  );
}