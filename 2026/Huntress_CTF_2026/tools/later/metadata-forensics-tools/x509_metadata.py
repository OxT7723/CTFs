#!/usr/bin/env python3
"""Read X.509 certificate metadata from PEM or DER bytes."""
from __future__ import annotations

import re

from cryptography import x509
from cryptography.hazmat.primitives import hashes


def _certificate(data: bytes) -> x509.Certificate:
    """Load the first certificate in a PEM bundle or a single DER certificate."""
    match = re.search(
        rb"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----",
        data,
        flags=re.DOTALL,
    )
    if match:
        return x509.load_pem_x509_certificate(match.group(0))
    return x509.load_der_x509_certificate(data)


def sha256_fingerprint(data: bytes) -> str:
    """Return the lowercase SHA-256 fingerprint of the certificate's DER form."""
    return _certificate(data).fingerprint(hashes.SHA256()).hex()
