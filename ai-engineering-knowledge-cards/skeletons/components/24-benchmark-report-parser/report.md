# CIS Kubernetes benchmark — fabricated run for this skeleton

## 1 Control plane components
[PASS] 1.1.1 Ensure that the API server pod specification file permissions are 600 or more restrictive
[FAIL] 1.2.5 Ensure that the --kubelet-certificate-authority argument is set as appropriate
[FAIL] 1.2.12 Ensure that the --enable-admission-plugins argument includes PodSecurity
[WARN] 1.2.9 Ensure that the admission control plugin EventRateLimit is set

## 2 Etcd node configuration
[PASS] 2.1 Ensure that the --cert-file and --key-file arguments are set as appropriate
[FAIL] 2.2 Ensure that the --client-cert-auth argument is set to true
[FAIL] 2.4 Ensure that the --peer-cert-file and --peer-key-file arguments are set as appropriate

## 3 Control plane configuration
[WARN] 3.2.1 Ensure that a minimal audit policy is created

## 4 Worker nodes
FAIL 4.2.1 Ensure that the --anonymous-auth argument is set to false
[FAIL] 4.2.6 Ensure that the --make-iptables-util-chains argument is set to true
[PASS] 4.1.1 Ensure that the kubelet service file permissions are 600 or more restrictive

## 5 Policies
[FAIL] 5.2.2 Minimize the admission of privileged containers (PodSecurityPolicy)
[WARN] 5.1.6 Ensure that service account tokens are only mounted where necessary
