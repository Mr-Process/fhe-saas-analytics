"""
Client-side SDK for FHE-based SaaS analytics service.

This module wraps the Pyfhel library to manage homomorphic encryption context,
key generation, encryption, and decryption. It abstracts away the complexities
of homomorphic encryption so client applications can work with plaintext data
while ensuring that only encrypted values are sent to the server.

The SDK uses the BFV and CKKS schemes available through Pyfhel. Use the BFV
scheme for exact integer arithmetic and the CKKS scheme for approximate real
valued computations.

Note: The Pyfhel dependency must be installed (see requirements.txt). This
SDK is a conceptual reference and may require further tuning for production.
"""

from typing import List, Any

try:
    # Pyfhel is a Python wrapper around the Microsoft SEAL library.  Importing
    # it here allows clients to call FHEClient only when the dependency is
    # available. When Pyfhel is not installed, the module still loads but
    # FHEClient will raise at runtime.
    from Pyfhel import Pyfhel, PyCtxt
except ImportError:
    Pyfhel = None  # type: ignore
    PyCtxt = Any   # type: ignore


class FHEClient:
    """
    Wrapper around Pyfhel to handle FHE key and encryption operations.

    The client is responsible for creating the encryption context, generating
    keys, encrypting plaintext values, and decrypting results returned by the
    server.  It never shares its secret key with the server.
    """

    def __init__(self, scheme: str = "CKKS", n: int = 2**14, scale: int = 2**30) -> None:
        """
        Initialise the FHE context and generate keys.

        :param scheme: 'CKKS' for real numbers or 'BFV' for integers.
        :param n: polynomial modulus degree, must be a power of two.
        :param scale: scaling factor for CKKS scheme.
        """
        if Pyfhel is None:
            raise ImportError(
                "Pyfhel is required for FHEClient. Install it via pip (e.g. pip install pyfhel)."
            )
        self.he = Pyfhel()
        # Initialize context parameters depending on scheme.  For CKKS we set
        # the modulus sizes for the coefficient modulus (qi_sizes) and the
        # scaling factor.  For BFV we choose a plaintext modulus p.
        if scheme.upper() == "CKKS":
            self.he.contextGen(scheme="CKKS", n=n, scale=scale, qi_sizes=[60, 40, 40, 60])
        elif scheme.upper() == "BFV":
            self.he.contextGen(p=65537, m=n, sec=128)
        else:
            raise ValueError("Unsupported scheme. Use 'CKKS' or 'BFV'.")
        # Generate secret key, public key, relinearization and rotation keys by default
        self.he.keyGen()

    def encrypt_list(self, values: List[float]) -> List['PyCtxt']:
        """
        Encrypt a list of numeric values.

        :param values: list of floats (CKKS) or ints (BFV).
        :return: list of ciphertext objects.
        """
        if self.he.is_scheme("CKKS"):
            return [self.he.encryptFrac([v]) for v in values]
        else:
            return [self.he.encryptInt(int(v)) for v in values]

    def decrypt_list(self, ciphertexts: List['PyCtxt']) -> List[float]:
        """
        Decrypt a list of ciphertexts.

        :param ciphertexts: list of ciphertext objects.
        :return: list of decoded floats or ints.
        """
        if self.he.is_scheme("CKKS"):
            return [float(self.he.decryptFrac(ctxt)[0]) for ctxt in ciphertexts]
        else:
            return [float(self.he.decryptInt(ctxt)) for ctxt in ciphertexts]

    def serialize_ciphertexts(self, ciphertexts: List['PyCtxt']) -> List[bytes]:
        """
        Serialize ciphertexts into bytes for transmission to the server.

        :param ciphertexts: list of ciphertext objects.
        :return: list of byte strings representing ciphertexts.
        """
        return [ctxt.to_bytes() for ctxt in ciphertexts]

    def deserialize_ciphertexts(self, data: List[bytes]) -> List['PyCtxt']:
        """
        Deserialize bytes back into ciphertext objects.

        :param data: list of byte strings.
        :return: list of ciphertext objects.
        """
        return [self.he.ciphertext_from_bytes(b) for b in data]
