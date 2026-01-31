"""
Weighted sum circuit v1 for FHE-based SaaS analytics.

This module defines a simple function for computing a weighted sum of
encrypted values using plaintext integer weights. The function
expects ciphertexts produced by Pyfhel encryption and uses the
homomorphic multiply_plain and add operations to compute the result.

The weighted sum computation is linear and has fixed depth, making
it suitable for homomorphic evaluation in BFV/BGV schemes.
"""

from typing import List
from Pyfhel import PyCtxt


def weighted_sum_v1(evaluator, ciphertexts: List[PyCtxt], weights: List[int]):
    """
    Compute a weighted sum of ciphertexts given integer weights.

    Args:
        evaluator: Instance of FHEEvaluator or similar with access to fhe context.
        ciphertexts: List of encrypted values (PyCtxt objects).
        weights: List of integers representing weights for each value.

    Returns:
        PyCtxt: Encrypted result representing the weighted sum.
    """
    if len(ciphertexts) != len(weights):
        raise ValueError("ciphertexts and weights must have the same length")
    result = None
    for ct, w in zip(ciphertexts, weights):
        # Multiply ciphertext by plaintext weight
        prod = evaluator.fhe.multiply_plain(ct, w)
        # Sum up products
        if result is None:
            result = prod
        else:
            result = evaluator.fhe.add(result, prod)
    return result
