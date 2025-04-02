# Migration Guide: Moving to the New Repository Structure

This guide explains how to migrate from the current structure to the new repository structure that meets the requirements.

## Current Structure

```
3-PythonApp/
├── app/
│   ├── app.py               # Python Flask application
│   ├── Dockerfile           # Container definition
│   └── requirements.txt     # Python dependencies
├── helm/
│   └── python-app/          # Helm chart for the app
├── argocd/
│   └── application.yaml     # ArgoCD Application resource
└── terraform/               # Infrastructure as code (Minikube-based)
```

## New Structure

```
blizzard-app/                # New repository name (on GitHub as Blizzardapp)
├── app/                     # Python application code
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── helm-chart/              # Helm templates for Kubernetes deployment
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
│       ├── deployment.yaml
│       ├── service.yaml
│       ├── ingress.yaml
│       └── secret.yaml
├── argocd/                  # ArgoCD ApplicationSet configuration
│   ├── applicationset.yaml
│   ├── certificate.yaml
│   └── cluster-issuer.yaml
├── aws/                     # AWS-specific resources
│   └── acm-certificate.yaml
└── .github/
    └── workflows/
        └── ci-cd.yaml       # GitHub Actions workflow
```

## Migration Steps

### 1. Create the New Repository

1. The repository has already been created at: https://github.com/AmichaiHadad/Blizzardapp.git
2. Clone it to your local machine:
   ```bash
   git clone https://github.com/AmichaiHadad/Blizzardapp.git
   cd Blizzardapp
   ```

### 2. Migrate Application Code

1. Copy the modified `app.py` to the new repository's `app/` directory.
2. Copy the modified `Dockerfile` to the new repository's `app/` directory.
3. Copy `requirements.txt` to the new repository's `app/` directory.

### 3. Migrate Helm Chart

1. Create a `helm-chart` directory in the new repository.
2. Copy the modified Helm chart files from this repository to the new repository:
   ```bash
   cp -r 3-PythonApp/helm-chart/* Blizzardapp/helm-chart/
   ```
3. Update the Helm values to use the Docker image: `amichaihadad2206/blizzard-app`

### 4. Copy ArgoCD Configuration

1. Create an `argocd` directory in the new repository.
2. Copy the relevant files:
   ```bash
   cp 3-PythonApp/argocd/applicationset.yaml Blizzardapp/argocd/
   cp 3-PythonApp/argocd/certificate.yaml Blizzardapp/argocd/
   cp 3-PythonApp/argocd/cluster-issuer.yaml Blizzardapp/argocd/
   ```
3. Update the `applicationset.yaml` file to use the correct repository URL: `https://github.com/AmichaiHadad/Blizzardapp.git`

### 5. Copy AWS Configuration

1. Create an `aws` directory in the new repository.
2. Copy the AWS configuration:
   ```bash
   cp 3-PythonApp/aws/acm-certificate.yaml Blizzardapp/aws/
   ```
3. Update the ACM certificate configuration to use the ARN: `arn:aws:acm:us-west-1:163459217187:certificate/fff7f866-c1e3-45f2-9520-e8fb9122fa81`

### 6. Copy GitHub Workflows

1. Create a `.github/workflows` directory in the new repository.
2. Copy the CI/CD workflow:
   ```bash
   mkdir -p Blizzardapp/.github/workflows
   cp 3-PythonApp/.github/workflows/ci-cd.yaml Blizzardapp/.github/workflows/
   ```
3. Update the workflow to use Docker Hub instead of ECR.
4. Add the following secrets to your GitHub repository:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username (amichaihadad2206)
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token

### 7. Push to GitHub

```bash
cd Blizzardapp
git add .
git commit -m "Initial commit"
git push origin main
```

### 8. Apply ArgoCD Configuration

Once the repository is ready:

```bash
kubectl apply -f argocd/cluster-issuer.yaml
kubectl apply -f argocd/applicationset.yaml
```

### 9. Verify Deployment

After ArgoCD syncs the application, verify it's accessible at https://app.blizzard.co.il 