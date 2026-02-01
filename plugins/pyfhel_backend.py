"""
Backend implementation using the existing FHEClient and FHEEvaluator.

This acts as an adapter so that the rest of the application can switch
between different FHE libraries via the plugins layer.
"""

from client.sdk import FHEClient
from server.evaluator import FHEEvaluator

class PyfhelBackend:
    def __init__(self, context_params: dict | None = None):
        # Default context parameters if none provided
        self.context_params = context_params or {"scheme": "CKKS", "n": 2**14, "scale": 2**30}
        self.client = FHEClient(self.context_params)
        self.evaluator = FHEEvaluator(self.context_params)

    def generate_keys(self):
        """Generate keys using the underlying FHE client."""
        self.client.generate_keys()

    def encrypt_list(self, values):
        """Encrypt a list of plaintext values."""
        return self.client.encrypt_list(values)

    def decrypt(self, ciphertexts):
        """Decrypt a list of ciphertexts."""
        return self.client.decrypt(ciphertexts)

    def deserialize_ciphertexts(self, enc_bytes):
        """Deserialize a list of ciphertext byte strings into ciphertext objects."""
        return self.evaluator.deserialize_ciphertexts(enc_bytes)

    def serialize_ciphertexts(self, ctxts):
        """Serialize ciphertext objects into byte strings."""
        return self.evaluator.serialize_ciphertexts(ctxts)

    def weighted_sum(self, enc_values, weights):
        """Compute a weighted sum on encrypted values using plaintext weights."""
        return self.evaluator.weighted_sum(enc_values, weights)
