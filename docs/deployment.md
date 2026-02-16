# Kubernetes Deployment Guide

This guide covers deploying the Apparatus System Harness to Kubernetes clusters for production use.

## Prerequisites

- Kubernetes cluster (1.20+)
- kubectl configured to access your cluster
- Helm 3.x (optional, for Helm deployment)
- Container registry access (for custom images)

## Container Images

Official images are available at:
```
ghcr.io/wadelabs/apparatus-system-harness:latest
ghcr.io/wadelabs/apparatus-system-harness:v0.1.0
ghcr.io/wadelabs/apparatus-system-harness:sha-<commit>
```

### Image Tags

- `latest` - Latest build from main branch
- `v*` - Stable release versions
- `sha-*` - Specific commit builds

## Quick Start with Helm

The fastest way to deploy is using the included Helm chart:

```bash
# Add the helm chart repository (if published)
helm repo add apparatus https://wadelabs.github.io/apparatus-system-harness

# Install with default values
helm install inquisitor apparatus/inquisitor

# Or install from local chart
helm install inquisitor deployments/kubernetes/helm/inquisitor
```

### Custom Values

Create a `values.yaml` file:

```yaml
image:
  repository: ghcr.io/wadelabs/apparatus-system-harness
  tag: v0.1.0
  pullPolicy: IfNotPresent

replicaCount: 3

resources:
  limits:
    cpu: 1000m
    memory: 2Gi
  requests:
    cpu: 500m
    memory: 1Gi

persistence:
  enabled: true
  storageClass: standard
  size: 10Gi

env:
  - name: LOG_LEVEL
    value: "INFO"
  - name: MANIFEST_DIR
    value: "/app/manifests"
```

Deploy with custom values:
```bash
helm install inquisitor apparatus/inquisitor -f values.yaml
```

## Manual Deployment

### 1. Create Namespace

```bash
kubectl create namespace inquisitor-system
```

### 2. Deploy ConfigMap

Create `configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: inquisitor-config
  namespace: inquisitor-system
data:
  LOG_LEVEL: "INFO"
  MANIFEST_DIR: "/app/manifests"
  ARTIFACT_DIR: "/app/artifacts"
```

Apply:
```bash
kubectl apply -f configmap.yaml
```

### 3. Create Persistent Volume Claims

Create `pvc.yaml`:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: inquisitor-manifests
  namespace: inquisitor-system
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: inquisitor-artifacts
  namespace: inquisitor-system
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

Apply:
```bash
kubectl apply -f pvc.yaml
```

### 4. Deploy StatefulSet (for Raft Cluster)

Create `statefulset.yaml`:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: inquisitor
  namespace: inquisitor-system
spec:
  serviceName: inquisitor-headless
  replicas: 3
  selector:
    matchLabels:
      app: inquisitor
  template:
    metadata:
      labels:
        app: inquisitor
    spec:
      containers:
      - name: inquisitor
        image: ghcr.io/wadelabs/apparatus-system-harness:latest
        ports:
        - containerPort: 8000
          name: http
        - containerPort: 4321
          name: raft
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        envFrom:
        - configMapRef:
            name: inquisitor-config
        volumeMounts:
        - name: manifests
          mountPath: /app/manifests
        - name: artifacts
          mountPath: /app/artifacts
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
      volumes:
      - name: manifests
        persistentVolumeClaim:
          claimName: inquisitor-manifests
      - name: artifacts
        persistentVolumeClaim:
          claimName: inquisitor-artifacts
```

Apply:
```bash
kubectl apply -f statefulset.yaml
```

### 5. Create Services

Create `service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: inquisitor
  namespace: inquisitor-system
spec:
  selector:
    app: inquisitor
  ports:
  - name: http
    port: 80
    targetPort: 8000
  type: LoadBalancer
---
apiVersion: v1
kind: Service
metadata:
  name: inquisitor-headless
  namespace: inquisitor-system
spec:
  clusterIP: None
  selector:
    app: inquisitor
  ports:
  - name: raft
    port: 4321
    targetPort: 4321
```

Apply:
```bash
kubectl apply -f service.yaml
```

## Raft Cluster Configuration

For production high availability with Raft consensus:

### Configure Raft Peers

Each pod needs to know about other pods in the cluster:

```yaml
env:
- name: RAFT_NODE_ID
  valueFrom:
    fieldRef:
      fieldPath: metadata.name
- name: RAFT_PEERS
  value: "inquisitor-0.inquisitor-headless:4321,inquisitor-1.inquisitor-headless:4321,inquisitor-2.inquisitor-headless:4321"
```

### Minimum Cluster Size

- **Minimum**: 3 nodes (tolerates 1 failure)
- **Recommended**: 5 nodes (tolerates 2 failures)
- **Formula**: 2f+1 nodes to tolerate f failures

## Monitoring and Observability

### Prometheus Metrics

The framework exposes Prometheus metrics on `/metrics`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: inquisitor-metrics
  namespace: inquisitor-system
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8000"
    prometheus.io/path: "/metrics"
spec:
  selector:
    app: inquisitor
  ports:
  - name: metrics
    port: 8000
```

### Key Metrics

- `inquisitor_manifest_validations_total` - Total manifest validations
- `inquisitor_manifest_validation_errors_total` - Validation errors
- `inquisitor_inquiry_executions_total` - Total inquiries executed
- `inquisitor_inquiry_duration_seconds` - Inquiry execution time
- `inquisitor_instrument_executions_total` - Instrument execution count
- `inquisitor_raft_leader` - Current Raft leader status

### Logging

Configure structured logging with JSON output:

```yaml
env:
- name: LOG_FORMAT
  value: "json"
- name: LOG_LEVEL
  value: "INFO"
```

Ship logs to your logging backend (e.g., ELK, Loki, CloudWatch).

## Scaling

### Horizontal Pod Autoscaling

For the API layer (non-Raft components):

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: inquisitor-hpa
  namespace: inquisitor-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: inquisitor-api
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Vertical Scaling

Adjust resource limits based on workload:

```yaml
resources:
  requests:
    memory: "2Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "2000m"
```

## Security

### RBAC Configuration

Create service account with minimal permissions:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: inquisitor
  namespace: inquisitor-system
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: inquisitor-role
  namespace: inquisitor-system
rules:
- apiGroups: [""]
  resources: ["configmaps", "secrets"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: inquisitor-binding
  namespace: inquisitor-system
subjects:
- kind: ServiceAccount
  name: inquisitor
  namespace: inquisitor-system
roleRef:
  kind: Role
  name: inquisitor-role
  apiGroup: rbac.authorization.k8s.io
```

### Network Policies

Restrict network access:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: inquisitor-netpol
  namespace: inquisitor-system
spec:
  podSelector:
    matchLabels:
      app: inquisitor
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: inquisitor-system
    ports:
    - protocol: TCP
      port: 8000
    - protocol: TCP
      port: 4321
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 53  # DNS
    - protocol: UDP
      port: 53  # DNS
```

### Secrets Management

Store sensitive data in Kubernetes secrets:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: inquisitor-secrets
  namespace: inquisitor-system
type: Opaque
stringData:
  api-key: "your-api-key"
  database-password: "your-db-password"
```

Reference in deployment:
```yaml
env:
- name: API_KEY
  valueFrom:
    secretKeyRef:
      name: inquisitor-secrets
      key: api-key
```

## Backup and Disaster Recovery

### Backup Strategy

1. **Manifests**: Store in Git (GitOps approach)
2. **Artifacts**: Regular PVC backups using Velero or similar
3. **Raft State**: Snapshot Raft logs periodically

### Velero Backup Example

```bash
# Install Velero (if not already installed)
velero install --provider aws --bucket my-backup-bucket

# Backup the namespace
velero backup create inquisitor-backup --include-namespaces inquisitor-system

# Schedule regular backups
velero schedule create inquisitor-daily --schedule="@daily" --include-namespaces inquisitor-system
```

## Upgrading

### Rolling Update

For zero-downtime upgrades:

```bash
# Update to new version
kubectl set image statefulset/inquisitor inquisitor=ghcr.io/wadelabs/apparatus-system-harness:v0.2.0 -n inquisitor-system

# Monitor rollout
kubectl rollout status statefulset/inquisitor -n inquisitor-system
```

### Rollback

If issues occur:

```bash
# Rollback to previous version
kubectl rollout undo statefulset/inquisitor -n inquisitor-system
```

## Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n inquisitor-system
kubectl describe pod <pod-name> -n inquisitor-system
```

### View Logs

```bash
kubectl logs <pod-name> -n inquisitor-system
kubectl logs <pod-name> -n inquisitor-system --previous  # Previous container
```

### Debug Container

```bash
kubectl exec -it <pod-name> -n inquisitor-system -- /bin/bash
```

### Check Raft Cluster Health

```bash
# Port-forward to leader
kubectl port-forward svc/inquisitor 8000:80 -n inquisitor-system

# Check cluster status
curl http://localhost:8000/raft/status
```

## Production Checklist

- [ ] Raft cluster with 3+ nodes deployed
- [ ] Persistent storage configured for manifests and artifacts
- [ ] Resource limits set appropriately
- [ ] Monitoring and alerting configured
- [ ] Logging pipeline established
- [ ] Backup strategy implemented
- [ ] Network policies applied
- [ ] RBAC configured with least privilege
- [ ] Secrets management in place
- [ ] Health checks configured
- [ ] Upgrade/rollback procedure tested

## Related Documentation

- [Architecture Overview](architecture.md)
- [Seven Layers Deep Dive](layers.md)
- [Manifest Schema Reference](manifest-schema.md)
- [Local Development Guide](local-quickstart.md)
