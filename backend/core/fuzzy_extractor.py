import secrets
import bchlib

# BCH configuration: 2048-bit input, t=10 error correction
# m=12 ensures the block size (4095) is large enough for our 2048-bit biometric vector
BCH_M = 12
BCH_T = 10
bch = bchlib.BCH(BCH_T, m=BCH_M)

def generate_sketch(bio_data: bytes):
    if len(bio_data) != 256:
        raise ValueError("bio_bits must be exactly 256 bytes")

    # Pad to 512 bytes for the BCH block size
    padded_data = bio_data + b'\x00' * 256 
    syndrome = bch.encode(padded_data)

    mask = secrets.token_bytes(256)
    hidden_seed = bytearray()
    for i in range(256):
        hidden_seed.append(bio_data[i] ^ mask[i])

    helper_data = syndrome + mask
    return bytes(hidden_seed), helper_data

def reproduce_sketch(noisy_bio: bytes, helper_data: bytes):

    print(f"DEBUG: Input length: {len(noisy_bio)}")
    print(f"DEBUG: First 5 bytes: {list(noisy_bio[:5])}")
    print(f"DEBUG: Helper data length: {len(helper_data)}")
    
    if len(noisy_bio) != 256:
        raise ValueError("bio_bits must be exactly 256 bytes")
        
    ecc_length = bch.ecc_bytes
    syndrome = bytearray(helper_data[:ecc_length])
    mask = helper_data[ecc_length:]
    
    noisy_array = noisy_bio
    
    errors = bch.decode(noisy_array, syndrome)
    
    if errors < 0:
        print(f"DEBUG: BCH Decode failed. Errors detected: {errors}")
        raise ValueError("reproduce_failed")
        
    bch.correct(noisy_array, syndrome)
    
    recovered_seed = bytearray()
    for i in range(256):
        recovered_seed.append(noisy_array[i] ^ mask[i])
        
    return bytes(recovered_seed)