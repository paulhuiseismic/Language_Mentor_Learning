# Docker Deployment Guide

## 🐳 Docker & Kubernetes Deployment for Language Mentor

This guide covers containerization and deployment options for the Language Mentor application.

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Docker Setup](#docker-setup)
- [Docker Compose](#docker-compose)
- [Kubernetes Deployment](#kubernetes-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Production Considerations](#production-considerations)

---

## 🚀 Quick Start

### Prerequisites
- Docker installed (version 20.10+)
- Docker Compose (version 2.0+)
- Azure OpenAI API credentials

### 1. Clone and Configure

```bash
# Clone the repository
git clone <your-repo-url>
cd Language_Mentor_Learning

# Copy environment template
cp .env.example .env

# Edit .env with your Azure OpenAI credentials
nano .env
```

### 2. Build and Run

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Or using Docker directly
docker build -t language-mentor:latest .
docker run -p 7860:7860 --env-file .env language-mentor:latest
```

### 3. Access the Application

Open your browser to: `http://localhost:7860`

---

## 🐳 Docker Setup

### Building the Image

```bash
# Build production image
docker build -t language-mentor:latest .

# Build with specific target
docker build --target testing -t language-mentor:test .

# Build with build args
docker build --build-arg PYTHON_VERSION=3.12 -t language-mentor:latest .
```

### Running the Container

```bash
# Basic run
docker run -p 7860:7860 \
  -e AZURE_OPENAI_API_KEY=your_key \
  -e AZURE_OPENAI_ENDPOINT=your_endpoint \
  language-mentor:latest

# Run with volume mounts
docker run -p 7860:7860 \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/prompts:/app/prompts:ro \
  language-mentor:latest

# Run in detached mode
docker run -d \
  --name language-mentor \
  --restart unless-stopped \
  -p 7860:7860 \
  --env-file .env \
  language-mentor:latest
```

### Multi-Stage Build Targets

The Dockerfile includes multiple build stages:

1. **base** - Base Python image with system dependencies
2. **dependencies** - Python packages installed
3. **testing** - Includes tests and runs them
4. **production** - Optimized production image

---

## 🎼 Docker Compose

### Basic Usage

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and start
docker-compose up -d --build
```

### Configuration

Edit `docker-compose.yml` to customize:

```yaml
services:
  language-mentor:
    environment:
      - AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}
      # Add more environment variables
    
    ports:
      - "7860:7860"  # Change port if needed
    
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

### Scaling

```bash
# Scale to multiple instances
docker-compose up -d --scale language-mentor=3

# With load balancer (requires additional setup)
docker-compose -f docker-compose.yml -f docker-compose.scale.yml up -d
```

---

## ☸️ Kubernetes Deployment

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace language-mentor

# Create secrets
kubectl create secret generic language-mentor-secrets \
  --from-literal=azure-openai-api-key=YOUR_KEY \
  --from-literal=azure-openai-endpoint=YOUR_ENDPOINT \
  -n language-mentor

# Apply deployment
kubectl apply -f kubernetes/deployment.yaml -n language-mentor

# Apply ingress (if using)
kubectl apply -f kubernetes/ingress.yaml -n language-mentor
```

### Verify Deployment

```bash
# Check pods
kubectl get pods -n language-mentor

# Check services
kubectl get svc -n language-mentor

# View logs
kubectl logs -f deployment/language-mentor -n language-mentor

# Check health
kubectl describe pod <pod-name> -n language-mentor
```

### Scaling

```bash
# Scale deployment
kubectl scale deployment language-mentor --replicas=5 -n language-mentor

# Auto-scaling
kubectl autoscale deployment language-mentor \
  --min=2 --max=10 --cpu-percent=80 \
  -n language-mentor
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

The repository includes two workflows:

#### 1. CI Workflow (`.github/workflows/ci.yml`)
- Runs on every push and PR
- Tests on multiple Python versions
- Runs linting checks
- Uploads coverage reports

#### 2. Docker Build & Push (`.github/workflows/docker-build-push.yml`)
- Builds and pushes Docker images
- Runs security scans with Trivy
- Pushes to GitHub Container Registry
- Tags images appropriately

### Azure DevOps

Use `azure-pipelines.yml` for Azure DevOps:

```bash
# Trigger pipeline
az pipelines run --name language-mentor-pipeline
```

### Setting Up Secrets

#### GitHub Secrets
```bash
# Add to repository secrets:
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_ENDPOINT
- DOCKERHUB_USERNAME (if using Docker Hub)
- DOCKERHUB_TOKEN
```

#### Kubernetes Secrets
```bash
# From file
kubectl create secret generic language-mentor-secrets \
  --from-env-file=.env \
  -n language-mentor

# From literal values
kubectl create secret generic language-mentor-secrets \
  --from-literal=azure-openai-api-key=YOUR_KEY \
  -n language-mentor
```

---

## 🏭 Production Considerations

### Security

1. **Non-root User**
   - Container runs as `appuser` (UID 1000)
   - No privileged access required

2. **Secrets Management**
   ```bash
   # Use Docker secrets
   docker secret create azure_api_key ./api_key.txt
   
   # Or Kubernetes secrets
   kubectl create secret generic api-credentials \
     --from-file=./credentials
   ```

3. **Image Scanning**
   ```bash
   # Scan with Trivy
   trivy image language-mentor:latest
   
   # Scan with Docker Scout
   docker scout cves language-mentor:latest
   ```

### Performance Optimization

1. **Resource Limits**
   ```yaml
   resources:
     requests:
       memory: "1Gi"
       cpu: "500m"
     limits:
       memory: "2Gi"
       cpu: "2000m"
   ```

2. **Caching**
   - Multi-stage builds cache dependencies
   - Use BuildKit for faster builds:
     ```bash
     DOCKER_BUILDKIT=1 docker build -t language-mentor:latest .
     ```

3. **Image Size**
   - Current image: ~1.5GB (optimized)
   - Using slim Python base
   - Multi-stage build removes build dependencies

### Monitoring

1. **Health Checks**
   ```bash
   # Docker health check
   docker inspect --format='{{.State.Health.Status}}' language-mentor
   
   # Kubernetes health
   kubectl get pods -n language-mentor
   ```

2. **Logging**
   ```bash
   # Docker logs
   docker logs -f language-mentor
   
   # Kubernetes logs
   kubectl logs -f deployment/language-mentor -n language-mentor
   ```

3. **Metrics**
   - Container metrics: `docker stats`
   - Kubernetes metrics: `kubectl top pods`

### High Availability

1. **Multiple Replicas**
   ```yaml
   spec:
     replicas: 3
   ```

2. **Rolling Updates**
   ```bash
   kubectl set image deployment/language-mentor \
     language-mentor=language-mentor:v2.0 \
     -n language-mentor
   ```

3. **Load Balancing**
   - Use Kubernetes Service (LoadBalancer type)
   - Or Ingress with NGINX/Traefik

---

## 📊 Troubleshooting

### Common Issues

1. **Container Won't Start**
   ```bash
   # Check logs
   docker logs language-mentor
   
   # Check environment variables
   docker exec language-mentor env
   ```

2. **Port Already in Use**
   ```bash
   # Change port mapping
   docker run -p 8080:7860 language-mentor:latest
   ```

3. **Out of Memory**
   ```bash
   # Increase Docker memory limit
   docker run --memory=4g language-mentor:latest
   ```

4. **Permission Issues**
   ```bash
   # Check file permissions
   docker exec language-mentor ls -la /app
   
   # Run with correct user
   docker run --user 1000:1000 language-mentor:latest
   ```

### Debug Mode

```bash
# Run with interactive shell
docker run -it --entrypoint /bin/bash language-mentor:latest

# Inside container, run manually
cd /app/src
python main.py
```

---

## 🔧 Advanced Configuration

### Custom Dockerfile

```dockerfile
# Build from specific tag
FROM language-mentor:latest as base

# Add custom dependencies
RUN pip install your-package

# Override entry point
CMD ["python", "custom_main.py"]
```

### Environment-Specific Configs

```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Azure DevOps Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/)

---

## 🆘 Support

For issues or questions:
1. Check the logs: `docker logs language-mentor`
2. Review health status: `docker inspect language-mentor`
3. Consult the main README.md
4. Open an issue on GitHub

---

**Last Updated:** November 25, 2025  
**Docker Version:** 20.10+  
**Kubernetes Version:** 1.25+  
**Status:** Production Ready ✅

