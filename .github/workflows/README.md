# GitHub Workflows Documentation

This repository contains a comprehensive set of GitHub Actions workflows designed to handle all possible scenarios for a Python microservice project.

## 🔄 Workflow Overview

### Core Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **CI Pipeline** (`ci.yml`) | Push, PR, Manual | Code quality, testing, security scanning |
| **CD Pipeline** (`cd.yml`) | Push to main, Tags, Manual | Build, deploy, release |
| **Release Management** (`release.yml`) | Push to main, Manual | Automated version bumping and releases |
| **Security & Dependencies** (`security.yml`) | Schedule, Push, PR, Manual | Security scans, dependency updates |
| **Branch Protection & Maintenance** (`maintenance.yml`) | Schedule, Push, PR, Manual | Repository maintenance, cleanup |
| **Hotfix Deployment** (`hotfix.yml`) | Hotfix branches, Manual | Emergency deployments |
| **Performance Testing** (`performance.yml`) | Schedule, Push, PR, Manual | Load testing, performance monitoring |

## 📋 Detailed Workflow Descriptions

### 1. CI Pipeline (`ci.yml`)

**Triggers:**
- Push to `main`, `master`, `develop` branches
- Pull requests to these branches
- Manual dispatch

**Jobs:**
- **Code Quality Checks**: Black, isort, Flake8, MyPy
- **Test Suite**: Multi-version Python testing (3.9, 3.10, 3.11)
- **Security Scan**: Safety, Bandit, CodeQL analysis
- **Docker Build**: Build and test Docker images
- **Integration Tests**: Database integration tests
- **Performance Tests**: Quick performance checks on PRs
- **Notifications**: Success/failure notifications

**Key Features:**
- ✅ Multi-Python version matrix testing
- ✅ Comprehensive security scanning
- ✅ Docker image testing
- ✅ Integration testing with PostgreSQL
- ✅ Code coverage reporting
- ✅ Performance regression detection

### 2. CD Pipeline (`cd.yml`)

**Triggers:**
- Push to `main`/`master` branches
- Release publications
- Version tags (`v*`)
- Manual deployment selection

**Jobs:**
- **Build & Push**: Docker image building and pushing to GHCR
- **Deploy Staging**: Automatic staging deployment
- **Deploy Production**: Production deployment (tags only)
- **Security Scan**: Container vulnerability scanning
- **Documentation**: Publish MkDocs to GitHub Pages
- **Rollback**: Automatic rollback on failure

**Key Features:**
- 🚀 Multi-platform Docker builds (AMD64, ARM64)
- 🔒 Security scanning with Trivy
- 📚 Automatic documentation publishing
- 🎯 Environment-specific deployments
- ⚡ Rollback capabilities
- 📱 Slack notifications

### 3. Release Management (`release.yml`)

**Triggers:**
- Push to main branch
- Manual release type selection

**Jobs:**
- **Change Detection**: Detect significant changes
- **Version Bumping**: Automatic semantic versioning
- **Release Creation**: GitHub releases with changelogs
- **Notifications**: Release notifications

**Key Features:**
- 🤖 Automatic version detection based on commit messages
- 📝 Changelog generation
- 🏷️ Git tagging
- 📢 Release notifications
- 📋 Post-release issue creation

**Semantic Versioning Rules:**
- `BREAKING CHANGE` or `breaking:` → Major version
- `feat` or `feature:` → Minor version
- Everything else → Patch version

### 4. Security & Dependencies (`security.yml`)

**Triggers:**
- Weekly schedule (Mondays 9 AM UTC)
- Dependency file changes
- Manual dispatch

**Jobs:**
- **Dependency Scanning**: Safety, pip-audit
- **Docker Security**: Trivy, Hadolint
- **Secret Detection**: TruffleHog scanning
- **License Compliance**: License checking
- **Automated Updates**: Dependency update PRs
- **Security Issues**: Automated issue creation

**Key Features:**
- 🔍 Multiple security scanning tools
- 🤖 Automated dependency updates
- 📄 License compliance checking
- 🕵️ Secret detection in code history
- 🚨 Security issue notifications
- ⚖️ Legal compliance monitoring

### 5. Branch Protection & Maintenance (`maintenance.yml`)

**Triggers:**
- Daily schedule (2 AM UTC)
- Branch pushes
- Pull request events
- Manual maintenance actions

**Jobs:**
- **Branch Protection**: Verify protection rules
- **PR Conventions**: Enforce naming conventions
- **Branch Cleanup**: Remove stale branches
- **Issue Management**: Mark stale issues/PRs
- **Repository Health**: Health check reports

**Key Features:**
- 🛡️ Branch protection verification
- 📏 PR title format enforcement
- 🧹 Automatic branch cleanup (30+ days old)
- 📊 Repository health monitoring
- 🏷️ Stale issue management
- 🔧 Automated maintenance tasks

### 6. Hotfix Deployment (`hotfix.yml`)

**Triggers:**
- Push to `hotfix/**` branches
- Manual hotfix deployment

**Jobs:**
- **Hotfix Validation**: Branch and version validation
- **Emergency Approval**: Required for emergency hotfixes
- **Quick Testing**: Critical tests only
- **Build & Deploy**: Fast-track deployment
- **Post-Deployment**: Merge back to main, documentation
- **Rollback Planning**: Automated rollback procedures

**Key Features:**
- 🚨 Emergency deployment capabilities
- ⚡ Fast-track testing and deployment
- 🔄 Automatic merge back to main
- 📋 Post-deployment checklists
- 🔙 Rollback plan generation
- 📢 Stakeholder notifications

**Hotfix Branch Naming:**
- `hotfix/description` - Standard hotfix
- `hotfix/emergency-description` - Emergency hotfix (requires approval)

### 7. Performance Testing (`performance.yml`)

**Triggers:**
- Daily schedule (3 AM UTC)
- Code changes in main
- Manual test selection

**Jobs:**
- **Environment Setup**: Test application deployment
- **Smoke Tests**: Basic performance validation
- **Load Tests**: Sustained load testing
- **Stress Tests**: Breaking point testing
- **Spike Tests**: Traffic spike handling
- **Database Tests**: Database performance testing
- **System Profiling**: CPU/Memory monitoring
- **Results Analysis**: Performance report generation

**Key Features:**
- 📊 Multiple test types (load, stress, spike, volume)
- 🔍 K6-based performance testing
- 📈 Performance trend monitoring
- 🎯 Automated threshold checking
- 📋 Detailed performance reports
- ⚠️ Performance regression alerts

## 🛠️ Setup Instructions

### 1. Repository Secrets

Add these secrets to your GitHub repository:

```
GITHUB_TOKEN          # Automatically provided
SLACK_WEBHOOK_URL     # Optional: Slack notifications
DOCKER_USERNAME       # Optional: If using Docker Hub
DOCKER_PASSWORD       # Optional: If using Docker Hub
```

### 2. Environment Setup

Create the following GitHub environments:

- `staging` - For staging deployments
- `production` - For production deployments (with protection rules)
- `emergency-approval` - For emergency hotfix approvals

### 3. Branch Protection Rules

The workflows will check for these branch protection settings:

- ✅ Require pull request reviews (≥1 approval)
- ✅ Dismiss stale reviews
- ✅ Require status checks to pass
- ✅ Require linear history
- ✅ Include administrators
- ✅ Restrict pushes

### 4. Required Status Checks

Configure these required status checks for main branch:

- `Code Quality Checks`
- `Test Suite (3.11)`
- `Security Scan`
- `Docker Build & Test`

## 🚀 Usage Examples

### Standard Development Flow

1. **Feature Development**:
   ```bash
   git checkout -b feat/new-feature
   # Make changes
   git push origin feat/new-feature
   # Create PR → Triggers CI pipeline
   ```

2. **Release Process**:
   ```bash
   git checkout main
   git merge feat/new-feature
   git push origin main
   # → Triggers CI, CD, and Release workflows
   ```

3. **Hotfix Process**:
   ```bash
   git checkout -b hotfix/critical-bug-fix
   # Make fixes
   git push origin hotfix/critical-bug-fix
   # → Triggers hotfix deployment workflow
   ```

### Manual Workflow Triggers

1. **Manual Deployment**:
   - Go to Actions → CD Pipeline → Run workflow
   - Select environment: `staging` or `production`

2. **Performance Testing**:
   - Go to Actions → Performance Testing → Run workflow
   - Select test type: `smoke`, `load`, `stress`, `spike`, `volume`
   - Configure users and duration

3. **Security Scan**:
   - Go to Actions → Security & Dependencies → Run workflow

4. **Maintenance Tasks**:
   - Go to Actions → Maintenance → Run workflow
   - Select action: `cleanup-branches`, `update-branch-protection`, etc.

## 📊 Monitoring and Alerts

### Automated Notifications

- 📱 **Slack Integration**: Deployment and security notifications
- 📧 **GitHub Issues**: Automated issue creation for problems
- 🏷️ **Labels**: Automatic labeling for different types of issues

### Performance Monitoring

- 📈 **Daily Performance Tests**: Automated performance regression detection
- 📊 **Performance Reports**: Weekly performance summary issues
- ⚠️ **Threshold Alerts**: Automatic alerts when performance degrades

### Security Monitoring

- 🔍 **Weekly Security Scans**: Dependency and container vulnerability scans
- 🚨 **Immediate Alerts**: Critical security issue notifications
- 📋 **Compliance Reports**: License and security compliance tracking

## 🔧 Customization

### Workflow Customization Points

1. **Python Versions**: Modify the matrix in `ci.yml`
2. **Performance Thresholds**: Adjust thresholds in `performance.yml`
3. **Security Tools**: Add/remove security scanning tools in `security.yml`
4. **Deployment Logic**: Replace placeholder deployment commands with actual deployment scripts
5. **Notification Channels**: Add Slack, Teams, or email notifications

### Environment Variables

Common environment variables used across workflows:

```yaml
PYTHON_VERSION: '3.11'        # Default Python version
REGISTRY: ghcr.io             # Container registry
IMAGE_NAME: ${{ github.repository }}  # Docker image name
```

### Branch Patterns

Supported branch patterns:

- `main` / `master` - Production branches
- `develop` - Development branch
- `feat/**` - Feature branches
- `fix/**` - Bug fix branches
- `hotfix/**` - Hotfix branches
- `release/**` - Release branches

## 🆘 Troubleshooting

### Common Issues

1. **Workflow Permissions**:
   - Ensure repository has necessary permissions for Actions
   - Check environment protection rules

2. **Secret Configuration**:
   - Verify all required secrets are set
   - Check secret naming and scope

3. **Branch Protection**:
   - Ensure branch protection rules match workflow requirements
   - Check admin enforcement settings

4. **Performance Tests**:
   - Verify application starts correctly in container
   - Check port binding and health endpoint

### Getting Help

1. Check workflow logs in GitHub Actions tab
2. Review this documentation for configuration details
3. Check individual workflow files for specific requirements
4. Create an issue if you find bugs or have suggestions

---

## 📝 Contributing

To improve these workflows:

1. Fork the repository
2. Create a feature branch: `feat/workflow-improvement`
3. Make your changes
4. Test thoroughly
5. Submit a pull request

The workflows will automatically test your changes and provide feedback.

---

**Note**: These workflows are designed to be comprehensive and may need customization based on your specific deployment environment and requirements. Replace placeholder deployment commands with your actual deployment logic.
