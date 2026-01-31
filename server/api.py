"""
Flask API for the FHE-SaaS-Analytics service.

This module exposes a REST endpoint for computing a weighted sum on
encrypted inputs. Clients submit base64-encoded ciphertexts and
plaintext weights; the server performs the homomorphic computation
and returns the result as a base64-encoded ciphertext. The server
never has access to plaintext data or secret keys.
"""

from flask import Flask, request, jsonify
import base64

from client.sdk import FHEClient
from server.evaluator import FHEEvaluator

# Default encryption parameters used by both client and server.
CONTEXT_PARAMS = {"scheme": "CKKS", "n": 2**14, "scale": 2**30}

app = Flask(__name__)

def _deserialize_ciphertexts(encoded_list):
    """Convert a list of base64 strings into raw byte strings."""
    return [base64.b64decode(s) for s in encoded_list]

def _serialize_ciphertext(ctxt_bytes: bytes) -> str:
    """Convert raw ciphertext bytes into a base64-encoded string."""
    return base64.b64encode(ctxt_bytes).decode("utf-8")

@app.route("/compute-weighted", methods=["POST"])
def compute_weighted():
    """Compute a weighted sum on encrypted inputs.

    Expects a JSON payload with two fields:
      - "ciphertexts": list of base64 strings representing encrypted values
      - "weights": list of numbers (same length as ciphertexts)

    Returns a JSON object with a single field:
      - "ciphertext": base64 string of the encrypted weighted sum
    """
    payload = request.get_json(force=True)
    enc_inputs_b64 = payload.get("ciphertexts")
    weights = payload.get("weights")

    if not isinstance(enc_inputs_b64, list) or not isinstance(weights, list):
        return jsonify({"error": "ciphertexts and weights must be lists"}), 400
    if len(enc_inputs_b64) != len(weights):
        return jsonify({"error": "ciphertexts and weights must be the same length"}), 400

    # Deserialize ciphertexts
    enc_bytes = _deserialize_ciphertexts(enc_inputs_b64)
    evaluator = FHEEvaluator(CONTEXT_PARAMS)
    enc_values = evaluator.deserialize_ciphertexts(enc_bytes)

    # Perform homomorphic weighted sum
    result_ctxt = evaluator.weighted_sum(enc_values, weights)

    # Serialize result back to client
    result_bytes = evaluator.serialize_ciphertexts([result_ctxt])[0]
    result_b64 = _serialize_ciphertext(result_bytes)
    return jsonify({"ciphertext": result_b64})


if __name__ == "__main__":
    # Run the API for local testing. In production, use a proper WSGI server.
    app.run(host="0.0.0.0", port=8000)
