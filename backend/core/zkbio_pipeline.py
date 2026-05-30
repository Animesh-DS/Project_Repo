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
