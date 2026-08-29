# Microservices Security Hardening Guide: Defense-in-Depth

## 1. Network & Container Hardening
1. **Container Execution**:
   - All Docker images run as unprivileged `node` user (UID 1000).
   - Read-only root filesystems enforced in Kubernetes deployment manifests (`readOnlyRootFilesystem: true`).
2. **Kubernetes Network Policies**:
   - Default-deny ingress and egress across all microservice namespaces.
   - Ingress only permitted from `api-gateway` pod labels.
3. **Secret Storage**:
   - Zero plain-text credentials in repository.
   - Kubernetes Secrets mounted dynamically as environment variables or encrypted file mounts.
