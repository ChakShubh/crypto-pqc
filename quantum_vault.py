"""
Post-Quantum Cryptography (PQC) & Hybrid Vault Service - File for Quantum Crypto Guard
Focus: NIST Standards (ML-KEM / FIPS 203, ML-DSA / FIPS 204) and Hybrid Key Exchange
"""
import base64
import os
import oqs 
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

class PostQuantumKEM:

    def __init__(self, kem_name: str = "ML-KEM-768"):
        """NIST Standardized Key Encapsulation Mechanism (FIPS 203 / Kyber-768)."""
        self.kem_name = kem_name

    def generate_and_encapsulate(self):
        """Quantum-Safe: Generates a PQC keypair and encapsulates a shared secret."""
        with oqs.KeyEncapsulation(self.kem_name) as client:
            public_key = client.generate_keypair()
            
            # Server encapsulates secret using client's public key
            with oqs.KeyEncapsulation(self.kem_name) as server:
                ciphertext, shared_secret_server = server.encap_secret(public_key)
                
            # Client decapsulates secret using private key
            shared_secret_client = client.decap_secret(ciphertext)
            
            assert shared_secret_client == shared_secret_server
            return public_key, ciphertext, shared_secret_client


class PostQuantumSigner:

    def __init__(self, sig_name: str = "ML-DSA-65"):
        """NIST Standardized Digital Signature Algorithm (FIPS 204 / Dilithium3)."""
        self.sig_name = sig_name

    def sign_payload(self, message: bytes) -> tuple:
        """Quantum-Safe: Signs payload using lattice-based digital signatures."""
        with oqs.Signature(self.sig_name) as signer:
            public_key = signer.generate_keypair()
            signature = signer.sign(message)
            return public_key, signature

    def verify_signature(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        """Quantum-Safe: Verifies ML-DSA signature."""
        with oqs.Signature(self.sig_name) as verifier:
            return verifier.verify(message, signature, public_key)


class HybridKeyExchange:

    def combine_ecdh_and_mlkem(self, peer_ecdh_pub, peer_mlkem_pub) -> bytes:
        """
        Transition Recommended: Hybrid Key Exchange.
        Combines classical ECDH (P-256) + ML-KEM-768 via HKDF to ensure security 
        against both classical implementation flaws and quantum attacks.
        """
        # 1. Classical ECDH Shared Secret
        ecdh_priv = ec.generate_private_key(ec.SECP256R1())
        ecdh_secret = ecdh_priv.exchange(ec.ECDH(), peer_ecdh_pub)
        
        # 2. PQC ML-KEM Shared Secret
        with oqs.KeyEncapsulation("ML-KEM-768") as server:
            _, pqc_secret = server.encap_secret(peer_mlkem_pub)
            
        # 3. Derive Composite Secret via HKDF
        composite_input = ecdh_secret + pqc_secret
        derived_hybrid_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'PQC-Hybrid-Handshake-v1',
        ).derive(composite_input)
        
        return derived_hybrid_key
