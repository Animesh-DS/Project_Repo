# ZK-BioAuth: Zero-Knowledge Biometric Pipeline

A high-performance, secure biometric authentication pipeline that uses **Zero-Knowledge Proofs (ZKP)** and **Fuzzy Extractors** to verify identity without ever storing raw images or permanent biometric templates.

## 🚀 The Core Philosophy
Traditional biometric systems are "honey-pots" for hackers. If a database is breached, facial data is compromised forever. This system converts biometric input into a **non-invertible mathematical commitment**. 

* **Zero-Knowledge:** No raw biometric data is ever stored.
* **Memory-Safe:** Raw biometric buffers are overwritten in RAM immediately after processing.
* **Error-Correcting:** Uses BCH codes to handle the "noise" inherent in human facial features.

## 🛠 Prerequisites
* Python 3.10+
* OpenCV & dlib (for landmark detection)
* A webcam with at least 720p resolution.

## ⚙️ Setup
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

   Download Model Weights:
Ensure dlib_face_recognition_resnet_model_v1.dat and shape_predictor_68_face_landmarks.dat are in your root directory.

📋 How to Use
1. Starting the Server
Run the FastAPI backend:

Bash
python main.py
2. Enrolment
Navigate to the frontend UI.

Click ENROL.

The system will capture a 2-second live frame, generate a cryptographic sketch, and create secure_vault.json.

The raw image is wiped from memory immediately upon completion.

3. Authentication
Click AUTHENTICATE.

The system captures a fresh frame.

The pipeline uses the helper_data from the vault to error-correct the new frame and hash the result.

If the hashes match, access is granted. If not, the UI triggers an ACCESS DENIED event.

🔐 Security Deep Dive
secure_vault.json: Stores only the BCH syndrome and the obfuscation mask. It is computationally infeasible to reverse this data to recreate the original face.

Memory Safety: We utilize ctypes.memset in our zero_bytes() utility to perform an OS-level wipe of RAM buffers, preventing cold-boot or memory-scraping attacks.

🧪 Troubleshooting
error_correct_failed: This indicates the BCH decoder could not reconcile the noise between your current face and the enrolled template. Ensure lighting and camera distance remain consistent with your Enrolment session.

Missing secure_vault.json: This file is auto-generated upon the first successful Enrolment.

Built for the [Hackathon Name] - Demonstrating the future of decentralized, privacy-preserving identity.