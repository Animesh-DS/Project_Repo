export default function JudgeNarrative({
  stages,
}) {

  /* ==========================================
     Human Explanation Layer

     This component explains
     cryptographic operations
     to judges.

     Driven entirely by backend
     stage events.

     P4 sends:

     capture
     preprocess
     error_correct
     hash
     wipe
     verify
  ========================================== */

  let message =
    "Waiting for authentication pipeline...";

  if (
    stages?.capture ===
    "done"
  ) {
    message =
      "Raw biometric loaded into RAM — never written to disk.";
  }

  if (
    stages?.preprocess ===
    "done"
  ) {
    message =
      "Biometric data normalised before cryptographic processing.";
  }

  if (
    stages?.error_correct ===
    "done"
  ) {
    message =
      "Fuzzy extractor corrects noise and derives a stable cryptographic key.";
  }

  if (
    stages?.hash ===
    "done"
  ) {
    message =
      "SHA-256 commitment generated. Original biometric key discarded.";
  }

  if (
    stages?.wipe ===
    "done"
  ) {
    message =
      "All intermediate memory overwritten with zeros. Biometric data no longer exists in RAM.";
  }

  if (
    stages?.verify ===
    "done"
  ) {
    message =
      "Commitment verified across decentralised nodes. No raw biometric data leaves the device.";
  }

  return (
    <div className="narrative-container">

      <div className="narrative-badge">
        LIVE EXPLANATION
      </div>

      <div className="narrative-text">
        {message}
      </div>

    </div>
  );
}