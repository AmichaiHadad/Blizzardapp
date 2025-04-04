# Blizzard Python Application on AWS EKS

This guide explains how to deploy the Blizzard Python application on an AWS EKS cluster using ArgoCD and AWS services for infrastructure management.

## Architecture Overview

The application deployment includes:

- Python Flask application containerized with Docker
- Docker Hub for container image storage (user: amichaihadad2206)
- AWS EKS for Kubernetes orchestration
- AWS ALB for load balancing and TLS termination
- AWS ACM for certificate management (pre-configured certificate)
- AWS Route53 for DNS management
- ArgoCD for GitOps-based continuous delivery

## Prerequisites

- AWS CLI configured with appropriate IAM permissions
- kubectl configured to access your EKS cluster
- AWS EKS cluster with "Services" node group (as per your infrastructure setup)
- Helm (v3+)
- ArgoCD installed on your EKS cluster
- Domain name (app.blizzard.co.il) configured in Route53
- AWS Secrets Store CSI Driver installed on your EKS cluster

## Deployment Steps

### 1. GitHub Repository Setup

The application code is hosted at: https://github.com/AmichaiHadad/Blizzardapp.git

To set up your own repository:
1. Fork the repository
2. Add the following secrets to your GitHub repository:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token (create from Docker Hub settings)

### 2. AWS Secrets Manager Configuration

This deployment uses AWS Secrets Manager to store sensitive configuration:

```bash
# Create the secret for OpenWeather API token
aws secretsmanager create-secret \
    --name openweather-api-token \
    --description "API token for OpenWeather service" \
    --secret-string "your-api-token-here"
```

The ARN of the created secret is:
`arn:aws:secretsmanager:us-west-1:163459217187:secret:openweather-api-token-rmLXm9`

This secret value will be mounted in the pod and also synchronized to a Kubernetes secret named `openweather-secret` with key `openweather-api-token`.

### 3. Certificate Configuration

This deployment uses a pre-configured ACM certificate:
- Certificate ARN: `arn:aws:acm:us-west-1:163459217187:certificate/fff7f866-c1e3-45f2-9520-e8fb9122fa81`
- Region: us-west-1

The certificate should be valid for the domain: app.blizzard.co.il

This certificate is used by the AWS ALB for TLS termination.

### 4. Deploy the Application with ArgoCD

```bash
# Apply the ApplicationSet configuration
kubectl apply -f argocd/applicationset.yaml
```

The ApplicationSet will automatically create an Application in ArgoCD that watches the GitHub repository for changes and deploys them to your cluster.

### 5. Verify the Deployment

1. Check that the application pods are running:

```bash
kubectl get pods -n blizzard-app
```

2. Check that the ALB Ingress has been created:

```bash
kubectl get ingress -n blizzard-app
```

3. Wait for DNS propagation and access the application at: https://app.blizzard.co.il

## CI/CD Pipeline

The CI/CD pipeline is implemented with GitHub Actions:

1. When code is pushed to the `main` branch, the workflow:
   - Builds the Docker image
   - Pushes it to Docker Hub
   - Updates the Helm chart with the new image tag
   - Commits the changes back to the repository

2. ArgoCD detects the changes in the Helm chart and automatically syncs the application.

## Monitoring and Troubleshooting

### Logs

```bash
# Get pod names
kubectl get pods -n blizzard-app

# View logs for a specific pod
kubectl logs <pod-name> -n blizzard-app
```

### ArgoCD Status

Check the application status in ArgoCD:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Then open a browser to https://localhost:8080 and log in to ArgoCD.

### Common Issues

1. **Application not accessible:**
   - Check ALB status in the AWS Console
   - Verify certificate is valid and correctly referenced in ingress.yaml
   - Check Route53 DNS records

2. **Pods not starting:**
   - Check pod status: `kubectl describe pod <pod-name> -n blizzard-app`
   - Verify node selector and tolerations match your EKS node group labels
   - Check if AWS Secrets Store CSI Driver is correctly installed and configured
   - Verify the SecretProviderClass deployment with: `kubectl get secretproviderclass -n blizzard-app`

3. **ArgoCD not syncing:**
   - Check ArgoCD logs: `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-application-controller`
   - Verify ApplicationSet configuration is correct

## Security Considerations

1. **Container Security:**
   - Non-root user in container
   - Read-only filesystem
   - No privilege escalation
   - Dropped capabilities

2. **Network Security:**
   - HTTPS only with TLS 1.2+
   - ALB configured for best security practices

3. **Secret Management:**
   - OpenWeather API token stored in AWS Secrets Manager
   - Secrets accessed via AWS Secrets Store CSI Driver
   - Docker Hub credentials stored as GitHub repository secrets

## Cleanup

To remove the deployment:

```bash
# Remove the ArgoCD ApplicationSet
kubectl delete -f argocd/applicationset.yaml

# Remove any other resources if needed
kubectl delete namespace blizzard-app
``` 