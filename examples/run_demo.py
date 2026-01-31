from client.sdk import FHEClient
from server.evaluator import FHEEvaluator


def main():
    """Run an end-to-end encrypted weighted sum demo."""
    # Example plaintext values (e.g. risk factors)
    values = [100.0, 50.0, 200.0]
    # Corresponding weights summing to 1.0
    weights = [0.4, 0.3, 0.3]

    # Initialize the client context and keys (CKKS scheme for real numbers)
    client = FHEClient(scheme="CKKS", n=2**14, scale=2**30)

    # Encrypt the plaintext values
    ciphertexts = client.encrypt_list(values)
    
    # Serialize ciphertexts to simulate sending to the server
    serialized = client.serialize_ciphertexts(ciphertexts)

    # Server-side: instantiate evaluator with matching context parameters
    context_params = {"scheme": "CKKS", "n": 2**14, "scale": 2**30}
    evaluator = FHEEvaluator(context_params)

    # Deserialize ciphertexts on the server
    enc_values = evaluator.deserialize_ciphertexts(serialized)

    # Compute the weighted sum homomorphically
    weighted_result_ctxt = evaluator.weighted_sum(enc_values, weights)

    # Serialize result to return to client
    result_bytes = evaluator.serialize_ciphertexts([weighted_result_ctxt])[0]

    # Client-side: deserialize and decrypt the result
    result_ctxt_client = client.deserialize_ciphertexts([result_bytes])[0]
    result_plain = client.decrypt_list([result_ctxt_client])[0]

    print("Weighted sum:", result_plain)


if __name__ == "__main__":
    main()
