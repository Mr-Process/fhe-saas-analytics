# Using the FHE-SaaS-Analytics Service

This guide explains how to set up the project locally and interact with the encrypted analytics API exposed by the service. The service uses Fully Homomorphic Encryption (FHE) so that all computations happen on encrypted data.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Mr-Process/fhe-saas-analytics.git
   cd fhe-saas-analytics
   ```
2. **Install dependencies** using Python 3.9+:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the API server** (development mode):
   ```bash
   python server/api.py
### Selecting a backend

The service now supports a pluggable FHE backend architecture. By default it uses the **Pyfhel** library, but you can switch to another supported backend by setting the `FHE_BACKEND` environment variable before starting the server.

For example, to run the server with the default backend:

```
bash
export FHE_BACKEND=pyfhel
python server/api.py
```

When additional backends are added to the `plugins` package, set `FHE_BACKEND` to the corresponding key (see `plugins/__init__.py`) to select that implementation.

   ```
   The server will start on `http://0.0.0.0:8000`. In production you should serve the `app` object in `server/api.py` with a proper WSGI server such as Gunicorn or uWSGI.

## Running the demo

To see an end‑to‑end encrypted computation without writing any client code, run the provided demo script:

```bash
python examples/run_demo.py
```

This script will:

- Generate an FHE context and keys on the client
- Encrypt a list of sample numeric values
- Compute a weighted sum homomorphically on the server
- Decrypt and print the result

## API Endpoint

Once the API server is running, you can send encrypted payloads to compute a weighted sum.

### `POST /compute-weighted`

**Request body** (JSON):

```json
{
  "ciphertexts": ["<base64 ciphertext>", "<base64 ciphertext>", ...],
  "weights": [0.4, 0.3, 0.3]
}
```

- `ciphertexts` should be a list of base64‑encoded ciphertexts representing your encrypted numeric inputs.
- `weights` should be a list of plaintext weights (floats or ints) of the same length as `ciphertexts`.

**Response body** (JSON):

```
{
  "ciphertext": "<base64 ciphertext result>"
}
```

The returned `ciphertext` is the encrypted weighted sum. It must be deserialized and decrypted by the client using their secret key.

### Workflow Summary

1. The client creates an instance of `FHEClient` and generates context and keys.
2. The client encrypts a list of numbers using `client.encrypt_list` and serializes the ciphertexts with `client.serialize_ciphertexts`. Convert each byte string to base64 for transport.
3. Send a `POST` request to `/compute-weighted` with the list of base64 ciphertexts and the corresponding weights.
4. The server computes the weighted sum homomorphically and returns the result as a base64 string.
5. The client converts the base64 string back to bytes, deserializes the ciphertext with `client.deserialize_ciphertexts`, and decrypts it using `client.decrypt_list`.

Example `curl` request (assuming you have two encrypted values):

```bash
curl -X POST http://localhost:8000/compute-weighted \
  -H "Content-Type: application/json" \
  -d '{
        "ciphertexts": ["<ctxt1_b64>", "<ctxt2_b64>"],
        "weights": [0.6, 0.4]
      }'
```

## Security Considerations

- **Never send plaintext** values to the API. Encrypt all inputs on the client side.
- The server operates purely on ciphertexts and **does not possess your secret keys**. Keep your secret key private.
- For sensitive deployments, run the server behind HTTPS and implement authentication, rate limiting, and audit logging.

---

For more information on how the FHE schemes work and design considerations, see `docs/research_fhe.md`.
