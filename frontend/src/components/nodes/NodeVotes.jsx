import { motion } from "framer-motion";

export default function NodeVotes({
  verifyResult,
}) {

  /* ==========================================
     Backend Contract

     verifyResult =

     {
       verified: true,
       node_votes:
       [true,true,true]
     }

     Sent by:

     verify/done

     P4 Owner:
     Animesh
  ========================================== */

  const votes =
    verifyResult?.node_votes ||
    [null, null, null];

  const verified =
    verifyResult?.verified;

  return (
    <>
      <div className="node-grid">

        {votes.map(
          (
            vote,
            index
          ) => (

            <motion.div
              key={index}
              className={`
                node-card
                ${
                  vote === true
                    ? "success"
                    : vote === false
                    ? "fail"
                    : ""
                }
              `}
              initial={{
                opacity: 0,
                y: 20,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
            >

              <h3>
                Node {index + 1}
              </h3>

              <div className="vote">

                {vote === true &&
                  "✓"}

                {vote === false &&
                  "✕"}

                {vote === null &&
                  "⟳"}

              </div>

            </motion.div>
          )
        )}

      </div>

      {verified !==
        undefined &&
        verified !==
          null && (

          <motion.div
            className={`
              verdict
              ${
                verified
                  ? "success"
                  : "fail"
              }
            `}
            initial={{
              opacity: 0,
              scale: 0.9,
            }}
            animate={{
              opacity: 1,
              scale: 1,
            }}
          >
            {verified
              ? "IDENTITY VERIFIED"
              : "ACCESS DENIED"}
          </motion.div>

      )}
    </>
  );
}