 # Threat Model for Zero-Knowledge Cancelable Biometrics Authentication System

## Introduction
This document outlines the threat model for the core cryptographic module of the Zero-Knowledge Cancelable Biometrics Authentication System. It details the security properties of the system, particularly focusing on the fuzzy extractor and cryptographic commitment layers.

## Security Properties

### 1. Computational Irreversibility of commitment_hex
The `commitment_hex` is derived from the `stable_key` using SHA-256, a cryptographic hash function. SHA-256 is designed to be a one-way function, meaning it is computationally infeasible to reverse the hashing process to obtain the original input (`stable_key`) from its hash output (`commitment_hex`). This property is known as preimage resistance.

### 2. Semantic Security of helper_data
The `helper_data` consists of the BCH error-correcting code's syndrome and a random nonce. The `stable_key` is derived from `bio_bits` XORed with a randomly generated nonce. Since the nonce is uniformly random, the `helper_data` does not leak sufficient information to reconstruct the `stable_key` or `bio_bits` without the corresponding live biometric input.

### 3. Biometric Cancellation
Biometric cancellation is achieved by incorporating a unique, randomly generated nonce during each enrolment. If a `commitment_hex` is compromised, the user can simply re-enroll, rendering the old hash useless.
## Attack Scenarios Considered

### 1. Stolen Hash Store
**Scenario:** An attacker gains access to the decentralized hash registry containing `commitment_hex` values.
**Mitigation:** The preimage resistance of SHA-256 prevents the attacker from deriving the `stable_key` or `bio_bits`. The hash serves only as a verification token, not a reversible identifier.

### 2. Compromised helper_data
**Scenario:** An attacker obtains `helper_data` associated with a user's enrolment.
**Mitigation:** The semantic security properties of the secure sketch (syndrome + random nonce) mean the `helper_data` alone does not leak biometric information. Without the live `bio_bits` from the user, it is mathematically insufficient to reconstruct the key.

### 3. Replay Attack
**Scenario:** An attacker intercepts a valid `stable_key` and attempts to use it for authentication.
**Mitigation:** The system relies on a fresh `bio_bits` input for each authentication attempt. A captured `stable_key` cannot bypass the biometric authentication process, as the pipeline mandates a successful `reproduce()` operation with a live, physical biometric sample within the t=10 error tolerance.