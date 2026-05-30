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
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            raise ValueError("capture_failed")
            
        dets = detector(frame, 1)
        if not dets:
            raise ValueError("no_face")
            
        shape = sp(frame, dets[0])
        face_descriptor = facerec.compute_face_descriptor(frame, shape)
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
    arr = np.clip(arr, -1.0, 1.0)
    
    quantised = (arr * 32767).astype('>i2')
    bio_bits_buf = bytearray(quantised.tobytes())
    
    if len(bio_bits_buf) != 256:
        raise ValueError("bad_capture_length")
        
    event_queue.put({"stage": "capture", "status": "done", "data": {"bytes_captured": 256}})
    event_queue.put({"stage": "preprocess", "status": "done", "data": {}})
    
    return bio_bits_buf