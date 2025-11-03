# Gary Reporter - Deployment Plan & Technical Roadmap

## Table of Contents
1. [Current State Assessment](#1-current-state-assessment)
2. [Target Architecture](#2-target-architecture)
3. [Migration Strategy](#3-migration-strategy)
4. [Infrastructure Setup](#4-infrastructure-setup)
5. [CI/CD Pipeline](#5-cicd-pipeline)
6. [Security & Compliance](#6-security--compliance)
7. [Monitoring & Operations](#7-monitoring--operations)
8. [Scaling Strategy](#8-scaling-strategy)
9. [Disaster Recovery](#9-disaster-recovery)
10. [Implementation Timeline](#10-implementation-timeline)

---

## 1. Current State Assessment

### Technical Debt Analysis

#### Critical Issues
- ❌ **Python 2.7 Support**: EOL since January 2020, security vulnerabilities
- ❌ **No Database**: Using local JSON files, not scalable
- ❌ **No Authentication**: No user management system
- ❌ **No Frontend**: Command-line only, no web interface
- ❌ **Hardcoded Credentials**: config.json with API keys in repository
- ❌ **No Error Handling**: Basic exception catching
- ❌ **Single-threaded**: No async operations
- ❌ **No API Documentation**: Undocumented REST endpoints

#### Major Issues
- ⚠️ **Python 3.5**: Outdated (current is 3.12), missing modern features
- ⚠️ **Flask**: Good framework but needs modernization
- ⚠️ **No Containerization**: Manual deployment, environment inconsistencies
- ⚠️ **No CI/CD**: Manual testing and deployment
- ⚠️ **Limited Testing**: Basic test coverage
- ⚠️ **Large Binary Files**: 80MB+ pickled corpus in repo

#### Minor Issues
- ℹ️ **Mixed Languages**: French and English documentation
- ℹ️ **Setup.py Mismatch**: Points to pocket-api, not gary-reporter
- ℹ️ **No Logging Strategy**: Basic file logging only
- ℹ️ **No Rate Limiting**: API can be abused

### Current Capabilities Worth Preserving
- ✅ **NLTK Integration**: Working NLP pipeline
- ✅ **Pocket API Wrapper**: Complete, functional implementation
- ✅ **Email System**: Working Mailgun integration with templates
- ✅ **Text Processing**: Bible tokenization and analysis works
- ✅ **Article Processing**: Core business logic is sound

---

## 2. Target Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
├──────────────────┬──────────────────┬──────────────────┬────────┤
│  Web App         │  Mobile App      │  CLI Tool        │  API   │
│  (Next.js)       │  (React Native)  │  (Python)        │ Clients│
└──────────────────┴──────────────────┴──────────────────┴────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Load Balancer   │
                    │   (AWS ALB/NLB)   │
                    └─────────┬─────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼────────┐   ┌────────▼────────┐   ┌──────▼──────┐
│  API Gateway   │   │  WebSocket      │   │   CDN       │
│  (Kong/AWS)    │   │  Server         │   │ (CloudFront)│
└───────┬────────┘   └────────┬────────┘   └─────────────┘
        │                     │
        └──────────┬──────────┘
                   │
        ┌──────────▼───────────┐
        │   Application Layer   │
        ├───────────────────────┤
        │  FastAPI Backend      │
        │  - REST API           │
        │  - GraphQL (optional) │
        │  - Authentication     │
        │  - Business Logic     │
        └──────────┬────────────┘
                   │
        ┌──────────┼──────────────────────┐
        │          │                      │
┌───────▼─────┐ ┌─▼────────────┐  ┌──────▼──────┐
│  Database   │ │  Cache Layer │  │   Queue     │
│  Layer      │ │              │  │   System    │
├─────────────┤ ├──────────────┤  ├─────────────┤
│ PostgreSQL  │ │  Redis       │  │  Celery +   │
│ (Users,     │ │  - Sessions  │  │  RabbitMQ   │
│  Billing)   │ │  - Cache     │  │  - NLP Jobs │
│             │ │  - Rate Limit│  │  - Emails   │
│ MongoDB     │ └──────────────┘  │  - Reports  │
│ (Documents, │                   └─────────────┘
│  Articles)  │
└─────────────┘
        │
┌───────▼──────────────────────────────────┐
│        External Services                  │
├───────────────────────────────────────────┤
│ • Auth0 (Authentication)                  │
│ • Stripe (Payments)                       │
│ • Mailgun (Email)                         │
│ • AWS S3 (File Storage)                   │
│ • Pocket API (Article Curation)           │
│ • Sentry (Error Tracking)                 │
│ • DataDog/CloudWatch (Monitoring)         │
│ • Intercom (Customer Support)             │
└───────────────────────────────────────────┘
```

### Technology Stack

#### Backend
```yaml
Language: Python 3.11+
Framework: FastAPI 0.104+
API Style: REST + GraphQL (optional)
ORM: SQLAlchemy 2.0 (PostgreSQL) + Motor (MongoDB)
Migration: Alembic
Task Queue: Celery 5.3+
Message Broker: RabbitMQ or Redis
NLP: NLTK 3.8+ + spaCy 3.7+ + HuggingFace Transformers
Testing: pytest, pytest-asyncio, pytest-cov
Code Quality: black, isort, mypy, ruff
```

#### Frontend
```yaml
Framework: Next.js 14 (React 18)
Language: TypeScript 5.2+
Styling: Tailwind CSS 3.3+
UI Components: Shadcn/ui + Radix UI
State Management: React Query + Zustand
Forms: React Hook Form + Zod
Charts: Recharts or Chart.js
Testing: Jest + React Testing Library + Playwright
```

#### Infrastructure
```yaml
Cloud Provider: AWS (primary) or GCP (alternative)
Container Runtime: Docker 24+
Orchestration: Kubernetes (EKS) or AWS ECS
IaC: Terraform 1.6+
CI/CD: GitHub Actions
Reverse Proxy: Nginx or Traefik
Load Balancer: AWS ALB/NLB
CDN: CloudFront or Cloudflare
```

#### Databases
```yaml
Relational: PostgreSQL 15+ (RDS)
  - Users, authentication
  - Subscriptions, billing
  - User settings
Document: MongoDB 7+ (Atlas or DocumentDB)
  - Research documents
  - Article content
  - NLP analysis results
Cache: Redis 7+ (ElastiCache)
  - Session storage
  - API response caching
  - Rate limiting
  - Real-time features
Search: Elasticsearch 8+ (optional, for advanced search)
```

#### Third-Party Services
```yaml
Authentication: Auth0 or AWS Cognito
Payments: Stripe
Email: Mailgun + SendGrid (backup)
File Storage: AWS S3
Error Tracking: Sentry
Monitoring: DataDog or AWS CloudWatch
Analytics: Mixpanel + Google Analytics
Support: Intercom or Zendesk
```

---

## 3. Migration Strategy

### Phase 1: Stabilization (Weeks 1-4)

#### Week 1-2: Setup & Assessment
- [ ] Set up development environment (Docker, local K8s)
- [ ] Audit all existing code and dependencies
- [ ] Document all API endpoints and functionality
- [ ] Create comprehensive test suite for existing features
- [ ] Set up version control best practices (branching strategy)

#### Week 3-4: Critical Updates
- [ ] **Upgrade to Python 3.11**
  - Update all syntax (print statements, exception handling)
  - Replace Python 2 libraries with Python 3 equivalents
  - Update requirements.txt with pinned versions
- [ ] **Extract configuration**
  - Create `.env.example` file
  - Use python-dotenv or pydantic-settings
  - Remove config.json from repository
- [ ] **Add pre-commit hooks**
  - black (formatting)
  - isort (import sorting)
  - mypy (type checking)
  - ruff (linting)

### Phase 2: Foundation (Weeks 5-12)

#### Database Layer (Weeks 5-7)
- [ ] **PostgreSQL Setup**
  - Design user schema (users, roles, permissions)
  - Design billing schema (subscriptions, invoices, payments)
  - Design settings schema (user preferences, API keys)
  - Create Alembic migrations
  - Implement SQLAlchemy models
  - Add connection pooling and retry logic

- [ ] **MongoDB Setup**
  - Design document schemas (research, articles, analysis)
  - Implement Motor (async MongoDB driver) integration
  - Add indexes for common queries
  - Implement TTL indexes for temporary data

- [ ] **Redis Setup**
  - Session storage implementation
  - Cache wrapper functions
  - Rate limiting middleware
  - Implement cache invalidation strategy

#### Authentication & Authorization (Week 8)
- [ ] **Auth0 Integration**
  - Set up Auth0 tenant
  - Configure social logins (Google, Facebook)
  - Implement JWT verification
  - Create role-based access control (RBAC)
  - Add API key authentication for programmatic access

- [ ] **User Management**
  - User registration flow
  - Email verification
  - Password reset
  - Profile management
  - API key generation

#### API Refactor (Weeks 9-10)
- [ ] **Migrate Flask to FastAPI**
  - Rewrite routes with FastAPI decorators
  - Add Pydantic models for request/response validation
  - Implement async endpoints
  - Add OpenAPI/Swagger documentation
  - Implement proper error handling and status codes

- [ ] **API Versioning**
  - Implement /api/v1 structure
  - Add deprecation warnings
  - Create API changelog

- [ ] **Rate Limiting**
  - Implement rate limiting per user tier
  - Add request throttling
  - Create usage tracking

#### Background Jobs (Weeks 11-12)
- [ ] **Celery Setup**
  - Configure RabbitMQ or Redis as broker
  - Create task modules (nlp, email, reports)
  - Implement periodic tasks (article fetching)
  - Add task monitoring (Flower)
  - Implement retry logic and error handling

### Phase 3: Feature Development (Weeks 13-20)

#### Frontend Application (Weeks 13-16)
- [ ] **Next.js Setup**
  - Initialize Next.js 14 project with App Router
  - Configure TypeScript and Tailwind
  - Set up authentication flow (Auth0)
  - Create component library (Shadcn/ui)
  - Implement routing structure

- [ ] **Core Pages**
  - Landing page
  - Login/signup
  - Dashboard
  - Search interface
  - Research workspace
  - Report builder
  - Settings page
  - Billing page

- [ ] **State Management**
  - Set up React Query for server state
  - Implement Zustand for client state
  - Add optimistic updates
  - Implement real-time updates (WebSocket)

#### Payment Integration (Week 17)
- [ ] **Stripe Setup**
  - Create products and pricing plans
  - Implement checkout flow
  - Add subscription management
  - Implement webhooks for events
  - Add invoice generation
  - Implement usage-based billing (metering)

#### Enhanced NLP Features (Weeks 18-20)
- [ ] **Modernize NLP Pipeline**
  - Add spaCy for entity recognition
  - Integrate HuggingFace models for embeddings
  - Implement semantic search
  - Add topic modeling
  - Create custom models for biblical entities

- [ ] **Async Processing**
  - Move NLP to Celery workers
  - Implement job status tracking
  - Add progress notifications
  - Create result caching

### Phase 4: Production Ready (Weeks 21-24)

#### Testing (Week 21)
- [ ] **Backend Tests**
  - Unit tests (pytest) - 80% coverage target
  - Integration tests (API endpoints)
  - Load tests (Locust or k6)
  - Security tests (OWASP ZAP)

- [ ] **Frontend Tests**
  - Unit tests (Jest)
  - Component tests (React Testing Library)
  - E2E tests (Playwright)
  - Visual regression tests (Percy or Chromatic)

#### Documentation (Week 22)
- [ ] **Developer Documentation**
  - Architecture documentation
  - API documentation (OpenAPI)
  - Setup guides
  - Contributing guidelines
  - Code style guide

- [ ] **User Documentation**
  - User guide
  - Tutorial videos
  - FAQ
  - API reference for developers

#### Security Hardening (Week 23)
- [ ] **Security Measures**
  - OWASP Top 10 audit
  - Dependency vulnerability scanning
  - Secrets management (AWS Secrets Manager)
  - SSL/TLS configuration
  - CORS configuration
  - CSP headers
  - SQL injection prevention
  - XSS prevention
  - CSRF protection

#### Performance Optimization (Week 24)
- [ ] **Backend Optimization**
  - Database query optimization
  - Add database indexes
  - Implement caching strategy
  - Connection pooling
  - CDN for static assets

- [ ] **Frontend Optimization**
  - Code splitting
  - Lazy loading
  - Image optimization (Next.js Image)
  - Bundle size optimization
  - Lighthouse score >90

---

## 4. Infrastructure Setup

### Development Environment

#### Local Development Stack
```yaml
# docker-compose.yml
version: '3.9'

services:
  # Backend API
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/gary_dev
      - MONGODB_URL=mongodb://mongo:27017/gary_dev
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - mongo
      - redis
    volumes:
      - ./backend:/app
    command: uvicorn main:app --reload --host 0.0.0.0

  # Frontend
  web:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules

  # PostgreSQL
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=gary
      - POSTGRES_PASSWORD=devpassword
      - POSTGRES_DB=gary_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # MongoDB
  mongo:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # RabbitMQ (for Celery)
  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"  # Management UI
    environment:
      - RABBITMQ_DEFAULT_USER=gary
      - RABBITMQ_DEFAULT_PASS=devpassword

  # Celery Worker
  celery:
    build: ./backend
    command: celery -A app.celery worker --loglevel=info
    depends_on:
      - rabbitmq
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/gary_dev
      - REDIS_URL=redis://redis:6379
      - CELERY_BROKER_URL=amqp://gary:devpassword@rabbitmq:5672

  # Celery Beat (for scheduled tasks)
  celery-beat:
    build: ./backend
    command: celery -A app.celery beat --loglevel=info
    depends_on:
      - rabbitmq
      - redis

  # Flower (Celery monitoring)
  flower:
    build: ./backend
    command: celery -A app.celery flower
    ports:
      - "5555:5555"
    depends_on:
      - celery
      - rabbitmq

volumes:
  postgres_data:
  mongo_data:
  redis_data:
```

### Staging Environment (AWS)

#### Architecture
- **VPC**: Private network with public and private subnets
- **ECS Fargate**: Serverless containers for API and workers
- **RDS**: PostgreSQL Multi-AZ deployment
- **DocumentDB**: MongoDB-compatible database
- **ElastiCache**: Redis cluster
- **Application Load Balancer**: Distribute traffic
- **S3**: Static asset storage
- **CloudFront**: CDN for frontend and static files
- **Route 53**: DNS management
- **ACM**: SSL certificates

#### Terraform Structure
```
infrastructure/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── production/
├── modules/
│   ├── vpc/
│   ├── ecs/
│   ├── rds/
│   ├── documentdb/
│   ├── elasticache/
│   ├── alb/
│   ├── s3/
│   ├── cloudfront/
│   └── monitoring/
└── main.tf
```

#### Sample Terraform (ECS Service)
```hcl
# infrastructure/modules/ecs/main.tf

resource "aws_ecs_cluster" "main" {
  name = "${var.environment}-gary-reporter-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "api" {
  family                   = "${var.environment}-gary-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.api_cpu
  memory                   = var.api_memory
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name  = "api"
    image = "${var.ecr_repository_url}:${var.image_tag}"

    portMappings = [{
      containerPort = 8000
      protocol      = "tcp"
    }]

    environment = [
      {
        name  = "ENVIRONMENT"
        value = var.environment
      },
      {
        name  = "DATABASE_URL"
        value = "postgresql://${var.db_username}:${var.db_password}@${var.db_endpoint}:5432/${var.db_name}"
      }
    ]

    secrets = [
      {
        name      = "AUTH0_CLIENT_SECRET"
        valueFrom = "${var.secrets_arn}:AUTH0_CLIENT_SECRET::"
      },
      {
        name      = "STRIPE_SECRET_KEY"
        valueFrom = "${var.secrets_arn}:STRIPE_SECRET_KEY::"
      }
    ]

    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/${var.environment}-gary-api"
        "awslogs-region"        = var.aws_region
        "awslogs-stream-prefix" = "ecs"
      }
    }

    healthCheck = {
      command     = ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"]
      interval    = 30
      timeout     = 5
      retries     = 3
      startPeriod = 60
    }
  }])
}

resource "aws_ecs_service" "api" {
  name            = "${var.environment}-gary-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = var.api_desired_count
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.api.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = var.target_group_arn
    container_name   = "api"
    container_port   = 8000
  }

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }

  enable_execute_command = true

  tags = {
    Environment = var.environment
    Application = "gary-reporter"
  }
}
```

### Production Environment

#### High-Availability Setup
- **Multi-Region**: Primary (us-east-1) + Failover (us-west-2)
- **Auto-scaling**: ECS services scale based on CPU/memory
- **Database**: Multi-AZ RDS with read replicas
- **CDN**: CloudFront with edge locations worldwide
- **Backup**: Automated daily backups with 30-day retention
- **Monitoring**: CloudWatch + DataDog for metrics and alerts

#### Resource Sizing (Production)

**API Service**
- **Instance Type**: Fargate 2 vCPU, 4GB RAM
- **Desired Count**: 4 (auto-scale 2-20)
- **Max Connections**: 1000 per instance

**Worker Service**
- **Instance Type**: Fargate 4 vCPU, 8GB RAM
- **Desired Count**: 2 (auto-scale 2-10)
- **Concurrency**: 10 tasks per worker

**Database (RDS PostgreSQL)**
- **Instance Type**: db.t3.large (2 vCPU, 8GB RAM)
- **Storage**: 100GB SSD (gp3)
- **Read Replicas**: 2
- **Backup**: Automated daily, 30-day retention

**Database (DocumentDB)**
- **Instance Type**: db.r5.large (2 vCPU, 16GB RAM)
- **Cluster**: 3 nodes (1 primary, 2 replicas)
- **Storage**: 100GB

**Cache (ElastiCache Redis)**
- **Node Type**: cache.r5.large (2 vCPU, 13.07GB RAM)
- **Cluster Mode**: Enabled
- **Nodes**: 3
- **Snapshots**: Daily automatic backups

---

## 5. CI/CD Pipeline

### GitHub Actions Workflow

#### Pull Request Workflow
```yaml
# .github/workflows/pr.yml
name: Pull Request

on:
  pull_request:
    branches: [main, develop]

jobs:
  # Backend tests
  backend-test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: testpass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run linters
        run: |
          cd backend
          black --check .
          isort --check .
          ruff check .
          mypy .

      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml --cov-report=term
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/test
          REDIS_URL: redis://localhost:6379

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml

  # Frontend tests
  frontend-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Run linter
        run: |
          cd frontend
          npm run lint

      - name: Run type check
        run: |
          cd frontend
          npm run type-check

      - name: Run unit tests
        run: |
          cd frontend
          npm run test:ci

      - name: Build
        run: |
          cd frontend
          npm run build
        env:
          NEXT_PUBLIC_API_URL: http://localhost:8000

  # Security scanning
  security:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

#### Deployment Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches:
      - main  # Production
      - develop  # Staging

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    outputs:
      image_tag: ${{ steps.meta.outputs.version }}

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Docker meta
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ steps.login-ecr.outputs.registry }}/gary-reporter
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build-and-push
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Update ECS service
        run: |
          aws ecs update-service \
            --cluster staging-gary-reporter-cluster \
            --service staging-gary-api \
            --force-new-deployment

      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster staging-gary-reporter-cluster \
            --services staging-gary-api

      - name: Run smoke tests
        run: |
          curl -f https://staging.garyreporter.com/health || exit 1

  deploy-production:
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Update ECS service (Blue/Green)
        run: |
          # Deploy to green environment
          aws ecs update-service \
            --cluster production-gary-reporter-cluster \
            --service production-gary-api-green \
            --force-new-deployment

      - name: Wait for green deployment
        run: |
          aws ecs wait services-stable \
            --cluster production-gary-reporter-cluster \
            --services production-gary-api-green

      - name: Run smoke tests on green
        run: |
          curl -f https://green.garyreporter.com/health || exit 1

      - name: Switch traffic to green
        run: |
          # Update ALB target group to point to green
          aws elbv2 modify-listener \
            --listener-arn ${{ secrets.PROD_LISTENER_ARN }} \
            --default-actions Type=forward,TargetGroupArn=${{ secrets.GREEN_TG_ARN }}

      - name: Monitor metrics
        run: |
          # Wait 5 minutes and check CloudWatch metrics
          sleep 300
          # Check error rate, latency, etc.

      - name: Notify Slack
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Production deployment successful! 🚀"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Deployment Strategy

#### Staging (Develop Branch)
- **Trigger**: Push to `develop` branch
- **Strategy**: Rolling update
- **Downtime**: None
- **Rollback**: Automatic on health check failure

#### Production (Main Branch)
- **Trigger**: Push to `main` branch (after PR review)
- **Strategy**: Blue/Green deployment
- **Downtime**: None
- **Rollback**: Switch back to previous version (< 1 minute)
- **Approval**: Manual approval required
- **Smoke Tests**: Automated tests before traffic switch

---

## 6. Security & Compliance

### Security Measures

#### Application Security
- [ ] **Authentication**
  - OAuth 2.0 / OpenID Connect (Auth0)
  - JWT with short expiration (15 minutes)
  - Refresh tokens with rotation
  - MFA support for premium users

- [ ] **Authorization**
  - Role-Based Access Control (RBAC)
  - Resource-level permissions
  - API key authentication for programmatic access
  - Rate limiting per user tier

- [ ] **Data Protection**
  - Encryption at rest (AES-256)
  - Encryption in transit (TLS 1.3)
  - Database encryption (RDS encryption)
  - Secrets management (AWS Secrets Manager)

- [ ] **API Security**
  - Input validation (Pydantic models)
  - SQL injection prevention (ORM + parameterized queries)
  - XSS prevention (Content Security Policy)
  - CSRF protection (SameSite cookies + tokens)
  - CORS configuration (whitelist)
  - Rate limiting (Redis-based)

#### Infrastructure Security
- [ ] **Network Security**
  - VPC with private subnets
  - Security groups (whitelist only)
  - WAF (Web Application Firewall)
  - DDoS protection (AWS Shield)

- [ ] **Access Control**
  - IAM roles (least privilege)
  - Multi-factor authentication for AWS
  - Bastion host for DB access
  - No hardcoded credentials
  - Secrets rotation (90 days)

- [ ] **Monitoring & Logging**
  - CloudTrail for AWS API calls
  - VPC Flow Logs
  - Application logs (CloudWatch)
  - Security incident alerts
  - SIEM integration (optional)

#### Compliance
- [ ] **GDPR Compliance** (if serving EU users)
  - Data privacy policy
  - User data export
  - Right to be forgotten
  - Cookie consent
  - Data processing agreements

- [ ] **SOC 2** (for enterprise customers)
  - Security controls documentation
  - Penetration testing (annual)
  - Vulnerability scanning (continuous)
  - Incident response plan
  - Third-party audits

- [ ] **PCI DSS** (for payment processing)
  - Stripe handles card data (PCI-compliant)
  - No card data stored
  - Secure webhooks

### Security Checklist

**Pre-Launch**
- [ ] Penetration testing completed
- [ ] Dependency vulnerability scan (Snyk/Dependabot)
- [ ] OWASP Top 10 audit
- [ ] Secrets removed from code
- [ ] SSL certificates configured
- [ ] Security headers configured
- [ ] Backup and disaster recovery tested

**Ongoing**
- [ ] Weekly dependency updates
- [ ] Monthly security reviews
- [ ] Quarterly penetration testing
- [ ] Annual security audits
- [ ] Incident response drills

---

## 7. Monitoring & Operations

### Observability Stack

#### Metrics (DataDog or CloudWatch)
- **Application Metrics**
  - Request rate, latency, error rate (RED metrics)
  - Database query performance
  - Cache hit rate
  - Task queue length
  - User activity metrics

- **Infrastructure Metrics**
  - CPU, memory, disk usage
  - Network I/O
  - Container health
  - Database connections
  - Lambda invocations (if used)

#### Logging (CloudWatch Logs or ELK Stack)
- **Structured Logging**
  - JSON format
  - Correlation IDs for request tracing
  - Log levels (DEBUG, INFO, WARN, ERROR)
  - User context (without PII)

- **Log Aggregation**
  - Centralized logging
  - Log retention (30 days standard, 1 year compliance)
  - Log search and filtering
  - Real-time log tailing

#### Tracing (AWS X-Ray or DataDog APM)
- Distributed tracing across services
- Database query tracing
- External API call tracing
- Performance bottleneck identification

#### Alerting

**Critical Alerts** (PagerDuty - 24/7 on-call)
- Service down (health check failures)
- Database connection failures
- High error rate (>5%)
- Payment processing failures
- Security incidents

**Warning Alerts** (Slack/Email)
- High latency (p95 > 1s)
- High CPU/memory (>80%)
- Low cache hit rate (<70%)
- Task queue backup (>1000 tasks)
- SSL certificate expiration (< 30 days)

**Info Alerts** (Slack)
- Deployment notifications
- New user signups
- High-value conversions
- Resource scaling events

### Dashboards

#### Operations Dashboard
- Service health status
- Request rate and latency
- Error rate by endpoint
- Active users
- Database performance
- Cache performance
- Task queue status

#### Business Dashboard
- New signups (daily/weekly/monthly)
- Active users (DAU/WAU/MAU)
- Conversion rate (free to paid)
- Revenue (MRR/ARR)
- Churn rate
- Feature usage
- Customer support tickets

### Runbooks

Create runbooks for common scenarios:
- [ ] Service outage response
- [ ] Database failover
- [ ] Rollback deployment
- [ ] Scale up/down resources
- [ ] Certificate renewal
- [ ] Backup restoration
- [ ] Security incident response

---

## 8. Scaling Strategy

### Vertical Scaling
- **API Service**: Start with 2 vCPU, scale to 8 vCPU
- **Database**: Start with db.t3.large, scale to db.r5.2xlarge
- **Cache**: Start with cache.r5.large, scale to cache.r5.4xlarge

### Horizontal Scaling

#### Application Tier
- **Auto-scaling Policy**
  - Scale out: CPU > 70% for 2 minutes
  - Scale in: CPU < 30% for 5 minutes
  - Min instances: 2
  - Max instances: 20

#### Database Tier
- **Read Replicas**: Add read replicas for read-heavy queries
- **Connection Pooling**: PgBouncer for PostgreSQL
- **Sharding**: Shard MongoDB by user_id (if needed)

#### Caching Strategy
- **Application Cache**: Redis for API responses (TTL 5-15 minutes)
- **Session Cache**: Redis for user sessions
- **CDN Cache**: CloudFront for static assets (TTL 1 day)
- **Database Query Cache**: Redis for expensive queries (TTL 1 hour)

### Performance Targets

| Metric | Target | Max |
|--------|--------|-----|
| API Latency (p50) | < 100ms | < 200ms |
| API Latency (p95) | < 500ms | < 1s |
| API Latency (p99) | < 1s | < 2s |
| Uptime | 99.9% | - |
| Error Rate | < 0.1% | < 1% |
| Time to First Byte | < 100ms | < 200ms |
| Page Load Time | < 2s | < 3s |

### Load Testing

**Tools**: Locust, k6, or Apache JMeter

**Test Scenarios**
- [ ] Normal load: 100 concurrent users
- [ ] Peak load: 500 concurrent users
- [ ] Stress test: 2,000 concurrent users
- [ ] Spike test: Sudden traffic increase
- [ ] Endurance test: 24-hour sustained load

**Test Frequency**
- Before major releases
- After infrastructure changes
- Monthly baseline tests

---

## 9. Disaster Recovery

### Backup Strategy

#### Database Backups
- **PostgreSQL (RDS)**
  - Automated daily backups (30-day retention)
  - Point-in-time recovery (5-minute intervals)
  - Manual snapshots before major changes
  - Cross-region backup replication

- **MongoDB (DocumentDB)**
  - Automated daily backups (30-day retention)
  - Manual snapshots before major changes

- **Redis (ElastiCache)**
  - Daily automatic backups
  - AOF (Append-Only File) persistence

#### Application Backups
- **Code**: Git (GitHub with branch protection)
- **Configuration**: Terraform state in S3 (versioned)
- **Secrets**: AWS Secrets Manager (automatic rotation)
- **User Files**: S3 with versioning enabled

### Recovery Procedures

#### Recovery Time Objective (RTO)
- **Critical Services**: < 1 hour
- **Non-Critical Services**: < 4 hours
- **Full System**: < 24 hours

#### Recovery Point Objective (RPO)
- **Database**: < 5 minutes (point-in-time recovery)
- **File Storage**: < 24 hours (S3 versioning)
- **Configuration**: < 1 hour (Terraform state)

### Disaster Scenarios

#### Scenario 1: Single Service Failure
- **Detection**: Health check failure, alerts triggered
- **Action**: Auto-restart container, alert on-call engineer
- **Recovery Time**: < 5 minutes (automatic)

#### Scenario 2: Database Failure
- **Detection**: Database connection failures
- **Action**: Automatic failover to standby (Multi-AZ)
- **Recovery Time**: < 2 minutes (automatic)

#### Scenario 3: Region Failure
- **Detection**: Multiple service failures, region-wide issues
- **Action**:
  1. Update DNS to point to backup region
  2. Restore latest database backup in backup region
  3. Deploy application in backup region
- **Recovery Time**: < 2 hours (manual)

#### Scenario 4: Data Corruption
- **Detection**: Anomalous data patterns, user reports
- **Action**:
  1. Identify corruption source and time
  2. Restore database from point-in-time backup
  3. Replay transactions if needed
- **Recovery Time**: < 4 hours (manual)

#### Scenario 5: Security Breach
- **Detection**: Security alerts, anomalous activity
- **Action**:
  1. Isolate affected systems
  2. Rotate all credentials
  3. Investigate breach
  4. Restore from clean backup
  5. Notify affected users
- **Recovery Time**: Varies (manual, priority #1)

### Testing

- **Quarterly**: DR drill (test database restore)
- **Bi-annually**: Full failover test to backup region
- **Annually**: Tabletop exercise for security breach

---

## 10. Implementation Timeline

### Overview: 6-Month Migration Plan

```
Month 1-2: Foundation & Planning
Month 3-4: Core Development
Month 5: Testing & Security
Month 6: Launch & Stabilization
```

### Detailed Timeline

#### Month 1: Foundation
**Week 1-2: Setup**
- [ ] Project kickoff and team onboarding
- [ ] Set up development environment (Docker)
- [ ] Configure AWS accounts (dev, staging, prod)
- [ ] Set up GitHub repository and branch protection
- [ ] Initialize Terraform infrastructure
- [ ] Set up CI/CD pipeline (GitHub Actions)

**Week 3-4: Code Modernization**
- [ ] Upgrade Python 2.7 → 3.11
- [ ] Extract configuration to environment variables
- [ ] Set up pre-commit hooks
- [ ] Create comprehensive test suite
- [ ] Document existing functionality

**Deliverables**:
- ✅ Modern development environment
- ✅ CI/CD pipeline operational
- ✅ Python 3.11 codebase with tests

---

#### Month 2: Database & Authentication
**Week 5-6: Database Layer**
- [ ] Design database schemas
- [ ] Set up PostgreSQL (local + RDS)
- [ ] Set up MongoDB (local + Atlas)
- [ ] Set up Redis (local + ElastiCache)
- [ ] Implement database models and migrations
- [ ] Create data migration scripts

**Week 7-8: Authentication**
- [ ] Configure Auth0 tenant
- [ ] Implement JWT authentication
- [ ] Create user management system
- [ ] Implement RBAC
- [ ] Add API key authentication

**Deliverables**:
- ✅ Database layer operational
- ✅ Authentication system working
- ✅ User management APIs

---

#### Month 3: API & Backend
**Week 9-10: API Refactor**
- [ ] Migrate Flask → FastAPI
- [ ] Add request/response validation (Pydantic)
- [ ] Implement async endpoints
- [ ] Add OpenAPI documentation
- [ ] Implement rate limiting
- [ ] Add error handling and logging

**Week 11-12: Background Jobs**
- [ ] Set up Celery + RabbitMQ
- [ ] Migrate article processing to Celery
- [ ] Migrate NLP processing to Celery
- [ ] Implement email queue
- [ ] Add task monitoring (Flower)

**Deliverables**:
- ✅ Modern FastAPI backend
- ✅ Background job processing
- ✅ API documentation

---

#### Month 4: Frontend & Payments
**Week 13-14: Frontend Foundation**
- [ ] Initialize Next.js project
- [ ] Set up design system (Tailwind + Shadcn)
- [ ] Implement authentication flow
- [ ] Create main layout and navigation
- [ ] Build landing page

**Week 15: Core Pages**
- [ ] Dashboard page
- [ ] Search interface
- [ ] Research workspace
- [ ] Settings page

**Week 16: Payment Integration**
- [ ] Configure Stripe products
- [ ] Implement checkout flow
- [ ] Add subscription management
- [ ] Implement webhooks
- [ ] Add billing page

**Deliverables**:
- ✅ Functional web application
- ✅ Payment processing working
- ✅ User-facing features

---

#### Month 5: Testing & Security
**Week 17-18: Testing**
- [ ] Backend unit tests (80% coverage)
- [ ] Backend integration tests
- [ ] Frontend unit tests
- [ ] E2E tests (Playwright)
- [ ] Load testing (k6)
- [ ] Fix identified bugs

**Week 19: Security Hardening**
- [ ] OWASP Top 10 audit
- [ ] Penetration testing
- [ ] Dependency vulnerability scan
- [ ] Security headers configuration
- [ ] Secrets management setup
- [ ] SSL/TLS configuration

**Week 20: Documentation & Training**
- [ ] Developer documentation
- [ ] API documentation
- [ ] User guide
- [ ] Admin runbooks
- [ ] Team training sessions

**Deliverables**:
- ✅ Comprehensive test coverage
- ✅ Security audit passed
- ✅ Complete documentation

---

#### Month 6: Launch Preparation & Go-Live
**Week 21: Beta Launch**
- [ ] Deploy to staging environment
- [ ] Invite 50 beta users
- [ ] Collect feedback
- [ ] Fix critical issues
- [ ] Performance optimization

**Week 22: Production Setup**
- [ ] Deploy infrastructure to production
- [ ] Configure monitoring and alerts
- [ ] Set up backup and DR
- [ ] Load testing on production-like environment
- [ ] Final security review

**Week 23: Soft Launch**
- [ ] Deploy to production
- [ ] Launch marketing website
- [ ] Open to limited public (100 users)
- [ ] Monitor metrics closely
- [ ] Iterate based on feedback

**Week 24: Full Launch & Stabilization**
- [ ] Public launch announcement
- [ ] Marketing campaign
- [ ] Customer support setup
- [ ] Monitor stability
- [ ] Address issues quickly

**Deliverables**:
- ✅ Production deployment
- ✅ Public launch
- ✅ Stable system with monitoring

---

### Post-Launch (Ongoing)

#### Month 7-12: Growth Phase
- Iterate on user feedback
- Add requested features
- Improve NLP capabilities
- Build mobile apps
- Scale infrastructure as needed
- Optimize costs
- Improve conversion rates

---

## Cost Estimates

### Development Costs (6 months)
| Resource | Cost |
|----------|------|
| 2 Senior Developers × $10K/mo × 6 | $120,000 |
| 1 Frontend Developer × $8K/mo × 4 | $32,000 |
| 1 DevOps Engineer × $10K/mo × 2 | $20,000 |
| 1 UX/UI Designer × $6K/mo × 2 | $12,000 |
| **Total Development** | **$184,000** |

### Infrastructure Costs (Monthly)

#### Staging Environment
| Service | Cost/Month |
|---------|------------|
| ECS Fargate (API + Workers) | $150 |
| RDS PostgreSQL (db.t3.medium) | $80 |
| DocumentDB (db.t3.medium) | $100 |
| ElastiCache Redis (cache.t3.small) | $30 |
| ALB | $25 |
| S3 + CloudFront | $20 |
| **Total Staging** | **~$405/month** |

#### Production Environment (Initial)
| Service | Cost/Month |
|---------|------------|
| ECS Fargate (4 API + 2 Workers) | $450 |
| RDS PostgreSQL (db.t3.large, Multi-AZ) | $300 |
| DocumentDB (db.r5.large, 3 nodes) | $800 |
| ElastiCache Redis (cache.r5.large) | $150 |
| ALB | $25 |
| S3 + CloudFront | $100 |
| Route 53 | $10 |
| ACM (SSL) | Free |
| CloudWatch Logs | $50 |
| Data Transfer | $100 |
| **Total Production (Initial)** | **~$1,985/month** |

#### Third-Party Services (Monthly)
| Service | Cost/Month |
|---------|------------|
| Auth0 | $0-240 (Free tier initially) |
| Stripe | 2.9% + $0.30 per transaction |
| Mailgun | $35 (50K emails) |
| Sentry | $26 (10K events) |
| DataDog | $0-31 (Free tier initially) |
| GitHub | Free (for small teams) |
| **Total Third-Party** | **~$61/month** |

### Total First Year Costs
- Development (6 months): $184,000
- Infrastructure (12 months): ~$30,000
- Third-party services (12 months): ~$1,000
- Marketing (as per business plan): $50,000
- **Total First Year**: **~$265,000**

---

## Success Criteria

### Technical Metrics
- [ ] 99.9% uptime
- [ ] < 200ms API latency (p95)
- [ ] Zero critical security vulnerabilities
- [ ] 80%+ code test coverage
- [ ] < 5% error rate

### Business Metrics
- [ ] 500+ paying users by end of Month 12
- [ ] $60K+ ARR by end of Month 12
- [ ] < 5% monthly churn rate
- [ ] > 10% free-to-paid conversion
- [ ] Net Promoter Score (NPS) > 40

---

## Conclusion

This deployment plan provides a comprehensive roadmap for transforming Gary Reporter from a personal Python script into a production-ready SaaS platform. The 6-month timeline is aggressive but achievable with a dedicated team.

**Critical Success Factors**:
1. ✅ **Team**: Hire experienced developers familiar with the tech stack
2. ✅ **Focus**: Prioritize MVP features, defer nice-to-haves
3. ✅ **Quality**: Don't compromise on security and testing
4. ✅ **Feedback**: Involve beta users early and iterate quickly
5. ✅ **Monitoring**: Instrument everything from day one

**Next Steps**:
1. Secure funding and assemble team
2. Begin Week 1 tasks immediately
3. Set up weekly check-ins to track progress
4. Establish clear communication channels
5. Start recruiting beta users

With disciplined execution and the right team, Gary Reporter can become the leading modern Bible research platform in the market.

---

**Document Version**: 1.0
**Last Updated**: November 3, 2025
**Prepared By**: AI DevOps & Architecture Assistant
