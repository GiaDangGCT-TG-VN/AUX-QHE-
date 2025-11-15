"""
CHE BFV Module
Classical Homomorphic Encryption using BFV scheme
Converted from che_bfv.ipynb notebook
"""

# Import BFV scheme for the classical homomorphic encryption component
# For more information refer to: https://github.com/sarojaerabelli/py-fhe/blob/master/examples/bfv_mult_example.py
from bfv.batch_encoder import BatchEncoder
from bfv.bfv_decryptor import BFVDecryptor
from bfv.bfv_encryptor import BFVEncryptor
from bfv.bfv_evaluator import BFVEvaluator
from bfv.bfv_key_generator import BFVKeyGenerator
from bfv.bfv_parameters import BFVParameters

def initialize_bfv_params(degree=8, plain_modulus=17, ciph_modulus=8000000000000):
    """
    Initialize BFV homomorphic encryption parameters.

    Args:
        degree (int): Polynomial degree for BFV scheme (default: 8)
        plain_modulus (int): Plain modulus for BFV scheme (default: 17)
        ciph_modulus (int): Cipher modulus for BFV scheme (default: 8000000000000)

    Returns:
        tuple: (params, encoder, encryptor, decryptor, evaluator)
    """
    params = BFVParameters(poly_degree=degree,
                          plain_modulus=plain_modulus,
                          ciph_modulus=ciph_modulus)
    key_generator = BFVKeyGenerator(params)
    public_key = key_generator.public_key
    secret_key = key_generator.secret_key
    relin_key = key_generator.relin_key
    encoder = BatchEncoder(params)
    encryptor = BFVEncryptor(params, public_key)
    decryptor = BFVDecryptor(params, secret_key)
    evaluator = BFVEvaluator(params)
    return params, encoder, encryptor, decryptor, evaluator
