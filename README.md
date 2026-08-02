# 🛡️ Crypto-PQC: Post-Quantum & Hybrid Encryption Reference Implementation

A reference repository demonstrating **NIST-standardized Post-Quantum Cryptography (PQC)** and hybrid classical-quantum transition models.

## 🎯 Purpose

This repository acts as a control testbed to verify that automated PQC auditors recognize modern quantum-resistant algorithms and hybrid key exchanges without flagging false positives.

## 🧪 Included Test Components

| Component | Standard / Standardized Implementation | Security Level | Audit Profile |
| :--- | :--- | :--- | :--- |
| **`PostQuantumKEM`** | **ML-KEM-768** (NIST FIPS 203 / Kyber) | Category 3 (AES-192 equivalent) | Quantum-Safe |
| **`PostQuantumSigner`** | **ML-DSA-65** (NIST FIPS 204 / Dilithium) | Category 3 | Quantum-Safe |
| **`HybridKeyExchange`** | **ECDH (P-256) + ML-KEM-768** via HKDF | Hybrid Defense-in-Depth | Recommended Transition Architecture |

## 🚀 Usage

Designed to be evaluated as a target compliant codebase by **QuantumCryptoGuardAgent**.
