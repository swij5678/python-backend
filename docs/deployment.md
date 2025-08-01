# Deployment Guide

This guide covers how to deploy the Python Service to various environments.

## Deployment Overview

The Python Service can be deployed using several methods:

- **Docker**: Containerized deployment
- **Kubernetes**: Orchestrated container deployment
- **Cloud Platforms**: AWS, Azure, GCP
- **Traditional Servers**: VM or bare metal deployment

## Prerequisites

- Docker (for containerized deployments)
- Kubernetes cluster (for K8s deployments)
- Cloud account (for cloud deployments)
- CI/CD pipeline setup

## Docker Deployment

### Building the Docker Image

```bash
# Build the image
docker build -t python-service:latest .

# Tag for registry
docker tag python-service:latest your-registry/python-service:v1.0.0
```

### Running with Docker

```bash
# Run single container
docker run -d \
  --name python-service \
  -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@db:5432/dbname" \
  python-service:latest

# Run with docker-compose
docker-compose up -d
```

### Docker Configuration Files

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["python", "src/main.py"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/pythonservice
      - DEBUG=false
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=pythonservice
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  postgres_data:
```

## Kubernetes Deployment

### Deployment Manifests

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: python-service
  labels:
    app: python-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: python-service
  template:
    metadata:
      labels:
        app: python-service
    spec:
      containers:
      - name: python-service
        image: your-registry/python-service:v1.0.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: python-service-secrets
              key: database-url
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
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: python-service
spec:
  selector:
    app: python-service
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

**ingress.yaml:**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: python-service-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  tls:
  - hosts:
    - api.yourdomain.com
    secretName: tls-secret
  rules:
  - host: api.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: python-service
            port:
              number: 80
```

### Deploying to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# Check logs
kubectl logs -f deployment/python-service

# Scale deployment
kubectl scale deployment python-service --replicas=5
```

## Cloud Deployments

### AWS Deployment

#### Using AWS App Runner

```bash
# Create apprunner.yaml
cat > apprunner.yaml << EOF
version: 1.0
runtime: python3
build:
  commands:
    build:
      - pip install -r requirements.txt
run:
  runtime-version: 3.9
  command: python src/main.py
  network:
    port: 8000
    env: PORT
  env:
    - name: DATABASE_URL
      value: "your-database-url"
EOF

# Deploy with AWS CLI
aws apprunner create-service --service-name python-service --source-configuration file://apprunner.yaml
```

#### Using ECS with Fargate

```bash
# Create task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster your-cluster \
  --service-name python-service \
  --task-definition python-service:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
```

### Azure Deployment

#### Using Azure Container Instances

```bash
# Create resource group
az group create --name python-service-rg --location eastus

# Deploy container
az container create \
  --resource-group python-service-rg \
  --name python-service \
  --image your-registry/python-service:latest \
  --ports 8000 \
  --environment-variables DATABASE_URL="your-database-url" \
  --restart-policy Always
```

#### Using Azure Container Apps

```bash
# Create container app environment
az containerapp env create \
  --name python-service-env \
  --resource-group python-service-rg \
  --location eastus

# Deploy container app
az containerapp create \
  --name python-service \
  --resource-group python-service-rg \
  --environment python-service-env \
  --image your-registry/python-service:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars DATABASE_URL="your-database-url"
```

### Google Cloud Platform

#### Using Cloud Run

```bash
# Deploy to Cloud Run
gcloud run deploy python-service \
  --image gcr.io/your-project/python-service:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL="your-database-url"
```

## Environment Configuration

### Production Environment Variables

```bash
# Application settings
DEBUG=false
LOG_LEVEL=INFO
PORT=8000

# Database
DATABASE_URL=postgresql://user:pass@host:port/db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=30

# Security
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com

# External services
REDIS_URL=redis://host:port/0
MONITORING_API_KEY=your-monitoring-key
```

### Secrets Management

#### Kubernetes Secrets

```bash
# Create secret
kubectl create secret generic python-service-secrets \
  --from-literal=database-url="postgresql://user:pass@host:port/db" \
  --from-literal=secret-key="your-secret-key"

# Use in deployment
env:
- name: DATABASE_URL
  valueFrom:
    secretKeyRef:
      name: python-service-secrets
      key: database-url
```

#### AWS Secrets Manager

```python
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client('secretsmanager', region_name='us-east-1')
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except ClientError as e:
        raise e
```

## Database Setup

### Database Migrations

```bash
# Run migrations in production
alembic upgrade head

# Create migration script for deployment
cat > migrate.sh << EOF
#!/bin/bash
set -e
echo "Running database migrations..."
alembic upgrade head
echo "Migrations completed successfully"
EOF

chmod +x migrate.sh
```

### Database Backup

```bash
# PostgreSQL backup
pg_dump $DATABASE_URL > backup.sql

# Restore from backup
psql $DATABASE_URL < backup.sql

# Automated backup script
cat > backup.sh << EOF
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL | gzip > backups/backup_$DATE.sql.gz
EOF
```

## Monitoring and Logging

### Health Checks

Implement comprehensive health checks:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/ready")
async def readiness_check():
    # Check database connection
    try:
        db.execute("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "error"
    
    return {
        "status": "ready" if db_status == "ok" else "not_ready",
        "checks": {
            "database": db_status
        }
    }
```

### Logging Configuration

```python
import logging
import sys

# Production logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/app/logs/app.log')
    ]
)
```

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    request_count.labels(method=request.method, endpoint=request.url.path).inc()
    request_duration.observe(duration)
    
    return response

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    - name: Run tests
      run: pytest --cov=src

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build Docker image
      run: |
        docker build -t python-service:${{ github.sha }} .
        docker tag python-service:${{ github.sha }} python-service:latest
    - name: Deploy to production
      run: |
        # Deploy using your preferred method
        echo "Deploying to production..."
```

## Performance Optimization

### Scaling Strategies

1. **Horizontal Scaling**: Add more instances
2. **Vertical Scaling**: Increase resources per instance
3. **Database Scaling**: Read replicas, connection pooling
4. **Caching**: Redis, in-memory caching

### Load Balancing

```nginx
# nginx.conf
upstream python_service {
    server app1:8000;
    server app2:8000;
    server app3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://python_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Security Considerations

### SSL/TLS Configuration

```bash
# Generate SSL certificate with Let's Encrypt
certbot certonly --webroot -w /var/www/html -d yourdomain.com
```

### Security Headers

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## Troubleshooting Deployments

### Common Issues

**Container Won't Start**
```bash
# Check logs
docker logs python-service

# Debug by running shell
docker run -it python-service:latest /bin/bash
```

**Database Connection Issues**
```bash
# Test database connectivity
python -c "import psycopg2; psycopg2.connect('your-database-url')"
```

**Resource Limits**
```bash
# Check resource usage
kubectl top pods
docker stats
```

### Rollback Procedures

```bash
# Kubernetes rollback
kubectl rollout undo deployment/python-service

# Docker rollback
docker-compose down
docker-compose up -d --scale app=0
docker-compose up -d
```

## Maintenance

### Zero-Downtime Deployments

1. Use rolling updates in Kubernetes
2. Implement health checks
3. Use load balancer health checks
4. Test deployments in staging first

### Regular Maintenance Tasks

- Monitor resource usage
- Update dependencies
- Rotate secrets
- Backup databases
- Review logs for errors
- Update security patches

For more information, see the [Development Guide](development.md) for local development practices.
