# ADR-017: Argon2id for Password Hashing and Key Derivation

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
Legacy hashing algorithms (MD5, SHA-1, SHA-256) and older slow hashes (bcrypt) are susceptible to GPU/ASIC-accelerated brute force attacks and side-channel vulnerabilities.

## Decision
We mandate **Argon2id** (winner of the Password Hashing Competition) for all credential hashing in the Auth Service.
- Memory cost: 64 MB (`65536 KiB`)
- Time cost: 3 iterations
- Parallelism: 4 threads
- Salt: 16 cryptographically secure random bytes

## Consequences
### Positive
- State-of-the-art resistance against GPU/ASIC side-channel and brute-force cracking attacks.
- Tunable memory and time parameters for future hardware advancements.

### Negative / Trade-offs
- Higher CPU and memory utilization during authentication requests (mitigated by rate limiting and worker offloading).
