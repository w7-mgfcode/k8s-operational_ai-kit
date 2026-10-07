# Glossary

Canonical terms for this platform. Use these exact terms in all output.
(Fabricated — every value below is invented for the prototype.)

| Term | Meaning |
|------|---------|
| **control plane** | 3 nodes behind the API endpoint `cp.example.test:6443` |
| **mesh-net** | The CNI, v1.9.4: eBPF networking, kube-proxy replacement |
| **block-store** | Default storage class, 3 replicas, retain on delete |
| **secrets-store consumers** | 18 apps read secrets through the sync operator |
| **log collector** | Node-level DaemonSet, v2.3.0 |
| **edge controller** | Legacy ingress controller, end of life Q3 2026 |
| **benchmark scan** | CIS scan as a CronJob, daily at 03:00 |
| **role tag** | Must equal the role directory name |
| **encrypted vars** | The secrets file, loaded explicitly on every run |
