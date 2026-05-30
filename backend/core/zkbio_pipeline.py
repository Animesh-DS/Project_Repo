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