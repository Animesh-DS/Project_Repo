import queue
import cv2
import dlib
import numpy as np
from typing import TypedDict, Literal
from zkbio_crypto import generate, reproduce, commit, zero_bytes

EnrolResult = TypedDict('EnrolResult', {
    'commitment_hex': str,
    'helper_data': bytes,
    'mode': Literal['enrol']
})

AuthResult = TypedDict('AuthResult', {
    'commitment_hex': str,
    'mode': Literal['auth']
})

PipelineEvent = TypedDict('PipelineEvent', {
    'stage': str,
    'status': str,
    'data': dict
})

event_queue: queue.Queue[PipelineEvent] = queue.Queue(maxsize=100)

def capture_biometric(mode: str = "face", filepath: str = "") -> bytearray:
    if mode == "face":
        cap = cv2.VideoCapture(0)
        
        for _ in range(5):
            cap.read()
            
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise ValueError("capture_failed")
            
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
        dets = detector(rgb_frame, 1)
       
        if len(dets) == 0:
            raise ValueError("no_face")
        elif len(dets) > 1:
            raise ValueError("multiple_faces_detected")
            
        shape = sp(rgb_frame, dets[0])
        face_descriptor = facerec.compute_face_descriptor(rgb_frame, shape)
        arr = np.array(face_descriptor, dtype=float)
        
    elif mode == "fingerprint":
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            raise ValueError("fingerprint_read_failed")
            
        arr = np.zeros(128, dtype=float)
        for i in range(8):
            k = cv2.getGaborKernel((31, 31), 4.0, i * np.pi / 8, 10.0, 0.5, 0, ktype=cv2.CV_32F)
            filtered = cv2.filter2D(img, cv2.CV_32F, k)
            
            pooled = cv2.resize(filtered, (4, 4))
            arr[i*16:(i+1)*16] = pooled.flatten()
            
    else:
        raise ValueError("invalid_mode")
    
  
    arr = np.nan_to_num(arr, nan=0.0, posinf=1.0, neginf=-1.0)
    
   
    norm = np.linalg.norm(arr)
    if norm > 0:
        arr = arr / norm
        
    arr = np.clip(arr, -1.0, 1.0)
    
    quantised = (arr * 32767).astype('>i2')
    bio_bits_buf = bytearray(quantised.tobytes())
    
    if len(bio_bits_buf) != 256:
        raise ValueError("bad_capture_length")
        
  
    event_queue.put({"stage": "capture", "status": "done", "data": {"bytes_captured": 256}})
    event_queue.put({"stage": "preprocess", "status": "done", "data": {}})
    
    return bio_bits_buf

def enrol(mode: str = "face") -> EnrolResult:
    bio_bits_buf = capture_biometric(mode)
    
    event_queue.put({"stage": "error_correct", "status": "start", "data": {}})
    stable_key, helper_data = generate(bytes(bio_bits_buf))
    event_queue.put({"stage": "error_correct", "status": "done", "data": {}})
    
    event_queue.put({"stage": "hash", "status": "start", "data": {}})
    commitment_hex = commit(stable_key)
    event_queue.put({"stage": "hash", "status": "done", "data": {"commitment_hex": commitment_hex[:8] + "..."}})
    
    event_queue.put({"stage": "wipe", "status": "start", "data": {}})
    zero_bytes(bio_bits_buf)
    stable_key_buf = bytearray(stable_key)
    zero_bytes(stable_key_buf)
    
    is_zero = all(b == 0 for b in bio_bits_buf)
    event_queue.put({"stage": "wipe", "status": "done", "data": {"verified_zero": is_zero}})
    
    return {"commitment_hex": commitment_hex, "helper_data": helper_data, "mode": "enrol"}