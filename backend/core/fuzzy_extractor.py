import secrets
import bchlib

bch = bchlib.BCH(10, m=12)

def generate_sketch(bio_data: bytes):
    syndrome = bch.encode(bio_data)
    
    mask = secrets.token_bytes(len(bio_data))
    
    hidden_seed = bytearray()
    for i in range(len(bio_data)):
        hidden_seed.append(bio_data[i] ^ mask[i])
    helper_data = syndrome + mask
    
    return bytes(hidden_seed), helper_data

def reproduce_sketch(noisy_bio: bytes, helper_data: bytes):
    ecc_length = bch.ecc_bytes
    syndrome = bytearray(helper_data[:ecc_length])
    mask = helper_data[ecc_length:]
    
    noisy_array = bytearray(noisy_bio)
    
    errors = bch.decode(noisy_array, syndrome)
    
    if errors < 0:
        raise ValueError("reproduce_failed")
        
    bch.correct(noisy_array, syndrome)
    
    recovered_seed = bytearray()
    for i in range(len(noisy_array)):
        recovered_seed.append(noisy_array[i] ^ mask[i])
        
    return bytes(recovered_seed)