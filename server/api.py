"""
Flask API for FHE-SaaS-Analytics using a pluggable backend.
This module exposes a REST endpoint for computing a weighted sum on
encrypted inputs. Clients submit base64-encoded ciphertexts and
plaintext weights; the server performs the homomorphic computation
and returns the result as a base64-encoded ciphertext. The server
never has access to plaintext data or secret keys.
"""

from flask import Flask, request, jsonify
import base64
import os

from plugins import get_backend

# Select backend via environment variable or default to Pyfhel
BACKEND_NAME = os.getenv("FHE_BACKEND", "pyfhel")
backend = get_backend(BACKEND_NAME)

app = Flask(__name__)

def _deserialize_ciphertexts(encoded_list):
    """Decode base64 strings and deserialize using the backend."""
    enc_bytes = [base64.b64decode(s) for s in encoded_list]
    return backend.deserialize_ciphertexts(enc_bytes)

def _serialize_ciphertext(ctxt):
    """Serialize ciphertext using backend and encode as base64 string."""
    # backend.serialize_ciphertexts expects a list of ciphertexts and returns list of bytes
    enc_bytes_list = backend.serialize_ciphertexts([ctxt])
    return base64.b64encode(enc_bytes_list[0]).decode("utf-8")

@app.route("/compute-weighted", methods=["POST"])
def compute_weighted():
    """Compute a weighted sum on encrypted inputs using the selected backend."""
    data = request.get_json()
    ciphertexts_b64 = data.get("ciphertexts")
    weights = data.get("weights")
    # Validate inputs
    if not isinstance(ciphertexts_b64, list) or not isinstance(weights, list) or len(ciphertexts_b64) != len(weights):
        return jsonify({"error": "Invalid input lengths"}), 400
    try:
        ctxts = _deserialize_ciphertexts(ciphertexts_b64)
        result_ctxt = backend.weighted_sum(ctxts, weights)
        result_b64 = _serialize_ciphertext(result_ctxt)
        return jsonify({"encrypted_result": result_b64})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
