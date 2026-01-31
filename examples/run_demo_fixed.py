"""
Demo script for fixed-point weighted sum using FHE SaaS analytics.

This example shows how a client can encrypt a list of real numbers using
fixed-point representation, send the encrypted values to the server for
homomorphic weighted sum computation, and decrypt the result.
"""

from client.sdk import FHEClient
from server.evaluator import FHEEvaluator
from server.circuits.weighted_sum_v1 import weighted_sum_v1


def main() -> None:
    # Instantiate client with BFV scheme for exact fixed-point arithmetic
    client = FHEClient(scheme="BFV")

    # Example values and integer weights
    values = [1.2, 3.4, 5.6]
    weights = [2, -1, 3]
    scale_factor = 10000

    # Encrypt values using fixed-point representation
    encrypted_values = client.encrypt_fixed_point(values, scale_factor=scale_factor)

    # Set up server evaluator with client's context
    evaluator = FHEEvaluator(client.he)

    # Perform weighted sum homomorphically
    result_ctxt = weighted_sum_v1(evaluator, encrypted_values, weights)

    # Decrypt result back to float
    result = client.decrypt_fixed_point([result_ctxt], scale_factor=scale_factor)[0]

    print(f"Weighted sum result: {result}")


if __name__ == "__main__":
    main()
