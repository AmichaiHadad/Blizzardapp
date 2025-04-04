# Blizzard Python Application

This repository contains a Python application designed for deployment on AWS EKS using ArgoCD for GitOps-based continuous delivery.

## Repository Information

- **GitHub Repository**: https://github.com/AmichaiHadad/Blizzardapp.git
- **Docker Image**: amichaihadad2206/blizzard-app

## Repository Structure

```
./
├── app/                     # Python application code
│   ├── app.py               # Main Flask application
│   ├── Dockerfile           # Container definition
│   └── requirements.txt     # Python dependencies
├── helm-chart/              # Helm templates for Kubernetes deployment
│   ├── Chart.yaml           # Chart metadata
│   ├── values.yaml          # Default configuration values
│   └── templates/           # Kubernetes resource templates
│       ├── deployment.yaml  # Pod deployment configuration
│       ├── service.yaml     # Service definition
│       ├── ingress.yaml     # Ingress with AWS ALB configuration
│       ├── secret.yaml      # Secret management (fallback)
│       └── secret-provider.yaml # AWS Secrets Manager integration
├── argocd/                  # ArgoCD configuration
│   ├── applicationset.yaml  # ApplicationSet for dynamic app deployment
│   ├── certificate.yaml     # TLS certificate configuration
│   └── cluster-issuer.yaml  # ClusterIssuer for certificate management
├── aws/                     # AWS-specific resources
│   └── acm-certificate.yaml # ACM certificate configuration
└── .github/
    └── workflows/
        └── ci-cd.yaml       # GitHub Actions workflow for CI/CD
```

## Application Description

The Python application serves dynamic content including:
- Client IP address display
- Welcome message
- Container name
- Current temperature in Tel-Aviv (fetched from OpenWeather API)

## Secret Management

This application uses AWS Secrets Manager for secure storage of API keys:
- Secret ARN: `arn:aws:secretsmanager:us-west-1:163459217187:secret:openweather-api-token-rmLXm9`
- Secret Content: OpenWeather API Token
- Integration: AWS Secrets Store CSI Driver

### Automated IAM Role Creation

The Helm chart includes an automated IAM role creation process:
1. On first installation, it checks if the required IAM role exists
2. If not, it automatically creates the IAM role with least-privilege permissions
3. It attaches a policy that only allows access to the specific secret
4. The service account is configured to use this role for AWS authentication

Prerequisites for this feature:
- An existing IAM role with permissions to create IAM roles and policies (specified in `values.yaml`)
- EKS cluster with OIDC provider configured for IAM roles for service accounts (IRSA)

## Certificate Information

This application uses a pre-configured ACM certificate:
- Certificate ARN: `arn:aws:acm:us-west-1:163459217187:certificate/fff7f866-c1e3-45f2-9520-e8fb9122fa81`
- Domain: app.blizzard.co.il

## Deployment

For detailed deployment instructions, please see [AWS-DEPLOYMENT.md](./AWS-DEPLOYMENT.md).

## Migration

For information on migrating from the legacy structure, see [MIGRATION-GUIDE.md](./MIGRATION-GUIDE.md). 