# PCI-DSS Level 1 Security & Compliance Architecture Matrix

## 1. Compliance Scope (SAQ A-EP)
NovaCommerce maintains strict isolation between customer payment data capture and internal database persistence.

| Requirement ID | PCI-DSS v4.0 Tenet | Technical Implementation & Safeguard | Verification Audit Method |
|:---|:---|:---|:---|
| **Req 1** | Firewall & Network Security | Kubernetes NetworkPolicies default-deny ingress/egress | Automated K8s policy audits |
| **Req 2** | Secure System Configurations | Hardened Distroless Alpine container base images | Trivy container vulnerability scanner |
| **Req 3** | Protect Cardholder Data | Direct browser-to-Stripe tokenization; Zero PAN storage | Static code AST data-flow analysis |
| **Req 4** | Encrypt Data in Transit | Mandatory TLS 1.3 with forward secrecy ciphers | Qualys SSL Labs A+ rating probe |
| **Req 5** | Antivirus & Malware Defense | Non-root read-only root filesystems on container pods | Falco runtime kernel monitoring |
| **Req 6** | Secure Software Development | Automated CI/CD security dependency audits | `npm audit` and Snyk security gates |
| **Req 7** | Need-to-Know Access Control | RBAC policy engine evaluating JWT user role claims | Automated Jest RBAC test suites |
| **Req 8** | Identify & Authenticate Users | Argon2id password hashing with mandatory MFA | Cryptographic parameter verification |
| **Req 9** | Restrict Physical Access | Hosted in Tier-4 SOC-2 certified cloud datacenters | Cloud provider compliance reports |
| **Req 10** | Log & Monitor Access | Immutable audit logs and distributed tracing | SIEM log forwarding with SHA-256 seals |
| **Req 11** | Regularly Test Security | Continuous blackbox synthetic security probes | Monthly third-party penetration tests |
| **Req 12** | Information Security Policy | Formalized Architecture Decision Records (ADRs) | SRE and SecOps committee sign-off |
