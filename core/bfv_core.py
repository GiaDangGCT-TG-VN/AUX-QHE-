"""
BFV Homomorphic Encryption Core Module

This module provides the basic BFV (Brakerski-Fan-Vercautern) homomorphic encryption
functionality for the AUX-QHE scheme.
"""

import logging
import sys
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def initialize_bfv_params(degree=8, plain_modulus=17, ciph_modulus=8000000000000):
    """
    Initialize BFV homomorphic encryption parameters.
    
    Args:
        degree (int): Polynomial degree for BFV scheme.
        plain_modulus (int): Plain modulus for BFV scheme.
        ciph_modulus (int): Cipher modulus for BFV scheme.
    
    Returns:
        tuple: (params, encoder, encryptor, decryptor, evaluator)
    """
    try:
        # First try to import from che_bfv notebook if available
        try:
            from che_bfv import initialize_bfv_params as init_bfv
            return init_bfv(degree, plain_modulus, ciph_modulus)
        except ImportError:
            pass
        
        # Alternative: Try importing from converted Python file
        try:
            import che_bfv
            return che_bfv.initialize_bfv_params(degree, plain_modulus, ciph_modulus)
        except ImportError:
            pass
        
        # Fallback: Create mock BFV implementation for testing
        logger.warning("che_bfv not found, using mock BFV implementation for testing")
        return create_mock_bfv_params(degree, plain_modulus, ciph_modulus)
        
    except Exception as e:
        logger.error(f"BFV initialization failed: {str(e)}")
        raise

def create_mock_bfv_params(degree=8, plain_modulus=17, ciph_modulus=8000000000000):
    """
    Create a mock BFV implementation for testing when che_bfv is not available.
    This is NOT cryptographically secure and should only be used for development.
    """
    logger.warning("Using MOCK BFV implementation - NOT CRYPTOGRAPHICALLY SECURE")
    
    class MockBFVParams:
        def __init__(self, degree, plain_modulus, ciph_modulus):
            self.poly_degree = degree
            self.plain_modulus = plain_modulus
            self.ciph_modulus = ciph_modulus
    
    class MockEncoder:
        def __init__(self, degree):
            self.degree = degree

        def encode(self, values):
            # Mock encoding - just return the input values
            return values[:self.degree] + [0] * (self.degree - len(values)) if len(values) < self.degree else values[:self.degree]

        def decode(self, encoded):
            # Mock decoding - just return the input
            return encoded if isinstance(encoded, list) else [encoded]
    
    class MockEncryptor:
        def __init__(self, encoder):
            self.encoder = encoder
            
        def encrypt(self, plaintext):
            # Mock encryption - deterministic for testing (no random noise)
            if isinstance(plaintext, list):
                return plaintext[:]  # Return copy to avoid reference issues
            else:
                return plaintext
    
    class MockDecryptor:
        def __init__(self, encoder):
            self.encoder = encoder
            
        def decrypt(self, ciphertext):
            # Mock decryption - deterministic (no rounding needed since no noise)
            if isinstance(ciphertext, list):
                return ciphertext[:]  # Return copy to avoid reference issues
            else:
                return ciphertext
    
    class MockEvaluator:
        def add(self, ct1, ct2):
            # Mock homomorphic addition
            if isinstance(ct1, list) and isinstance(ct2, list):
                return [x + y for x, y in zip(ct1, ct2)]
            else:
                return ct1 + ct2
        
        def multiply(self, ct1, ct2):
            # Mock homomorphic multiplication
            if isinstance(ct1, list) and isinstance(ct2, list):
                return [x * y for x, y in zip(ct1, ct2)]
            else:
                return ct1 * ct2
    
    # Create mock objects
    params = MockBFVParams(degree, plain_modulus, ciph_modulus)
    encoder = MockEncoder(degree)
    encryptor = MockEncryptor(encoder)
    decryptor = MockDecryptor(encoder)
    evaluator = MockEvaluator()
    
    logger.info(f"Mock BFV initialized: degree={degree}, plain_modulus={plain_modulus}")
    
    return params, encoder, encryptor, decryptor, evaluator

def run_bfv_tests(mod_value=2, test_iterations=3):
    """
    Run homomorphic encryption tests for the BFV scheme.

    Args:
        mod_value (int): Modulo value for arithmetic (default: 2 for binary).
        test_iterations (int): Number of iterations for multiple addition test (default: 3).

    Returns:
        dict: Test results with test names and pass/fail status.
    """
    results = {}
    try:
        # Initialize CHE components
        params, encoder, encryptor, decryptor, evaluator = initialize_bfv_params()
        poly_degree = params.poly_degree
        logger.info(f"Initialized with polynomial degree: {poly_degree}")

        def encode_value(value, length):
            """Encode a value into a padded list for encryption."""
            return encoder.encode([value] + [0] * (length - 1))

        # Test 1: Encoding and decoding
        value = 1
        try:
            encoded = encode_value(value, poly_degree)
            encrypted = encryptor.encrypt(encoded)
            decrypted = decryptor.decrypt(encrypted)
            decoded = encoder.decode(decrypted)[0] % mod_value
            results['test_encoding_decoding'] = decoded == value
            logger.info(f"Test 1: Input {value}, Decoded {decoded}, {'Pass' if decoded == value else 'Fail'}")
        except Exception as e:
            logger.error(f"Test 1 failed: {str(e)}")
            results['test_encoding_decoding'] = False

        # Test 2: Homomorphic addition (1 + 1 = 0 mod 2)
        try:
            enc_1 = encryptor.encrypt(encode_value(1, poly_degree))
            enc_1_again = encryptor.encrypt(encode_value(1, poly_degree))
            sum_enc = evaluator.add(enc_1, enc_1_again)
            sum_decoded = encoder.decode(decryptor.decrypt(sum_enc))[0] % mod_value
            expected = (1 + 1) % mod_value
            results['test_homomorphic_addition'] = sum_decoded == expected
            logger.info(f"Test 2: 1 + 1 = {sum_decoded} mod {mod_value}, {'Pass' if sum_decoded == expected else 'Fail'}")
        except Exception as e:
            logger.error(f"Test 2 failed: {str(e)}")
            results['test_homomorphic_addition'] = False

        # Test 3: Multiple additions
        try:
            enc_0 = encryptor.encrypt(encode_value(0, poly_degree))
            enc_sum = encryptor.encrypt(encode_value(1, poly_degree))
            for _ in range(test_iterations):
                enc_sum = evaluator.add(enc_sum, enc_0)
            final_decoded = encoder.decode(decryptor.decrypt(enc_sum))[0] % mod_value
            results['test_multiple_additions'] = final_decoded == 1
            logger.info(f"Test 3: 1 + {'0 + ' * (test_iterations - 1)}0 = {final_decoded} mod {mod_value}, {'Pass' if final_decoded == 1 else 'Fail'}")
        except Exception as e:
            logger.error(f"Test 3 failed: {str(e)}")
            results['test_multiple_additions'] = False

        return results

    except Exception as e:
        logger.error(f"Initialization failed: {str(e)}")
        return {'initialization': False}

if __name__ == "__main__":
    test_results = run_bfv_tests()
    logger.info(f"BFV Test Results: {test_results}")