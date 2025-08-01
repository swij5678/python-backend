# Python Service

A sample Python service with comprehensive documentation and configuration.

## Overview

This is a sample Python microservice that demonstrates best practices for:
- Project structure
- Documentation with MkDocs
- Service catalog integration
- Testing and development workflows

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the service:
   ```bash
   python src/main.py
   ```

3. Run tests:
   ```bash
   pytest
   ```

## Documentation

Full documentation is available in the `docs/` folder and can be served with:

```bash
mkdocs serve
```

## Development

This project uses:
- Python 3.9+
- FastAPI for the web framework
- Pytest for testing
- MkDocs for documentation
- Pre-commit hooks for code quality

## Service Catalog

This service is registered in the service catalog via `catalog-info.yaml`.
