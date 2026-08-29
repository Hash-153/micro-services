# Zero-Trust Microservice Network Security & mTLS Policy

## 1. Network Topology
All microservice-to-microservice traffic is governed by Kubernetes NetworkPolicies enforcing default-deny ingress and egress rules.

1. **Ingress Controller**: Only component exposed to external public traffic on ports 80/443.
2. **API Gateway**: Sole entity authorized to send HTTP requests to internal microservice REST ports.
3. **Internal Microservices**: Isolated within Kubernetes cluster namespace with mutual TLS (mTLS) cryptographic encryption.
