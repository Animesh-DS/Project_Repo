export default function JudgeNarrative({
  currentStage,
}) {

  const messages = {
    capture:
      "Raw biometric loaded into RAM. Never written to disk.",

    preprocess:
      "Biometric normalized before cryptographic processing.",

    error_correct:
      "Fuzzy extractor corrects noise and derives stable key.",

    hash:
      "SHA-256 commitment generated. Original key discarded.",

    wipe:
      "All intermediate memory overwritten with zeros.",
  };

  return (
    <div className="narrative-text">
      {messages[currentStage] ||
        "Waiting for pipeline..."}
    </div>
  );
}