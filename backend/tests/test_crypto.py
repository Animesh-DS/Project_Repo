import unittest
import secrets
import sys
import os

# Quick hack to get the imports working for testing
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.fuzzy_extractor import generate_sketch, reproduce_sketch

class TestFuzzyExtractor(unittest.TestCase):
    def setUp(self):
        self.bio_bits = secrets.token_bytes(256)

    def test_exact_match(self):
        seed1, helper = generate_sketch(self.bio_bits)
        seed2 = reproduce_sketch(self.bio_bits, helper)
        self.assertEqual(seed1, seed2)

    def test_small_errors(self):
        seed1, helper = generate_sketch(self.bio_bits)
        
        # Flip 3 bits
        noisy = bytearray(self.bio_bits)
        for i in range(3):
            noisy[i] ^= 1
            
        seed2 = reproduce_sketch(bytes(noisy), helper)
        self.assertEqual(seed1, seed2)

    def test_too_many_errors(self):
        _, helper = generate_sketch(self.bio_bits)
        
        noisy = bytearray(self.bio_bits)
        for i in range(15):  # t=10, so 15 should fail
            noisy[i] ^= 1
            
        # The leader's spec says this MUST raise a ValueError specifically.
        # Let's see if my draft does that...
        print("\nDEBUG: Running too_many_errors test... why is it raising a generic Exception?")
        with self.assertRaises(ValueError):
            reproduce_sketch(bytes(noisy), helper)

    def test_strict_length(self):
        # The spec says exactly 256 bytes!
        short_bio = secrets.token_bytes(255)
        with self.assertRaises(ValueError):
            generate_sketch(short_bio)

if __name__ == '__main__':
    unittest.main()