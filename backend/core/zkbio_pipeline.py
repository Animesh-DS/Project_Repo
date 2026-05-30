import queue
import cv2
import dlib
import numpy as np
import threading
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



detector = dlib.get_frontal_face_detector()
facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")
sp = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


camera_lock = threading.Lock()

def _safe_push(event: PipelineEvent) -> None:
    """Helper to instantly push events without freezing FastAPI if the queue is full."""
    try:
        event_queue.put_nowait(event)
    except queue.Full:
        pass

def capture_biometric(mode: str = "face", filepath: str = "") -> bytearray:
    if mode == "face":
        # Block concurrent threads from accessing the camera simultaneously
        with camera_lock:
            cap = cv2.VideoCapture(0)
            try:
                for _ in range(5):
                    cap.read()
                ret, frame = cap.read()
            finally:
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
        
    _safe_push({"stage": "capture", "status": "done", "data": {"bytes_captured": 256}})
    _safe_push({"stage": "preprocess", "status": "done", "data": {}})
    
    return bio_bits_buf


def enrol(mode: str = "face") -> EnrolResult:
    commitment_hex = ""
    helper_data = b""
    bio_bits_buf = None
    stable_key = None
    current_stage = "capture"  
    
    try:
        bio_bits_buf = capture_biometric(mode)
        
        current_stage = "error_correct"
        _safe_push({"stage": current_stage, "status": "start", "data": {}})
        stable_key, helper_data = generate(bytes(bio_bits_buf))
        _safe_push({"stage": current_stage, "status": "done", "data": {}})
        
        current_stage = "hash"
        _safe_push({"stage": current_stage, "status": "start", "data": {}})
        commitment_hex = commit(stable_key)
        _safe_push({"stage": current_stage, "status": "done", "data": {"commitment_hex": commitment_hex[:8] + "..."}})
        
    except Exception:
        _safe_push({"stage": current_stage, "status": "error", "data": {"error": f"{current_stage}_failed"}})
        
    finally:
        _safe_push({"stage": "wipe", "status": "start", "data": {}})
        is_zero = True
        
        try:
            if bio_bits_buf is not None:
                zero_bytes(bio_bits_buf)
                is_zero = all(b == 0 for b in bio_bits_buf)
        except Exception:
            is_zero = False  
            
        try:
            if stable_key is not None:
                del stable_key
        except Exception:
            pass
            
        _safe_push({"stage": "wipe", "status": "done", "data": {"verified_zero": is_zero}})
        
    return {"commitment_hex": commitment_hex, "helper_data": helper_data, "mode": "enrol"}


def authenticate(helper_data: bytes, commitment_hex: str, mode: str = "face") -> AuthResult:
    candidate_hex = ""
    bio_bits_buf = None
    stable_key = None
    current_stage = "capture"
    
    try:
        bio_bits_buf = capture_biometric(mode)
        
        current_stage = "error_correct"
        _safe_push({"stage": current_stage, "status": "start", "data": {}})
        stable_key = reproduce(bytes(bio_bits_buf), helper_data)
        _safe_push({"stage": current_stage, "status": "done", "data": {}})
        
        current_stage = "hash"
        _safe_push({"stage": current_stage, "status": "start", "data": {}})
        candidate_hex = commit(stable_key)
        _safe_push({"stage": current_stage, "status": "done", "data": {"commitment_hex": candidate_hex[:8] + "..."}})
        
    except Exception:
        _safe_push({"stage": current_stage, "status": "error", "data": {"error": f"{current_stage}_failed"}})
        
    finally:
        _safe_push({"stage": "wipe", "status": "start", "data": {}})
        is_zero = True
        
        try:
            if bio_bits_buf is not None:
                zero_bytes(bio_bits_buf)
                is_zero = all(b == 0 for b in bio_bits_buf)
        except Exception:
            is_zero = False
            
        try:
            if stable_key is not None:
                del stable_key
        except Exception:
            pass
            
        _safe_push({"stage": "wipe", "status": "done", "data": {"verified_zero": is_zero}})
        
    return {"commitment_hex": candidate_hex, "mode": "auth"}