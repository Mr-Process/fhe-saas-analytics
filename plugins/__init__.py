"""
Plugin layer for FHE backends.

This module selects and initializes FHE backend implementations.
Currently only PyfhelBackend is available.
"""

from .pyfhel_backend import PyfhelBackend

# Registry of available backends
BACKENDS = {
    "pyfhel": PyfhelBackend,
}

def get_backend(name: str = "pyfhel", context_params: dict | None = None):
    """
    Return an instance of the chosen FHE backend.

    Args:
        name: Name of the backend to use.
        context_params: Dictionary of encryption parameters.

    Raises:
        ValueError: If an unknown backend name is provided.
    """
    backend_cls = BACKENDS.get(name)
    if backend_cls is None:
        raise ValueError(f"Unknown backend: {name}")
    return backend_cls(context_params or {})
