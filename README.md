# pagopa-qa-superset

This repository contains the customized [Apache Superset](https://superset.apache.org/) deployment used to expose analytical dashboards.

The project is the presentation layer for operational and analytical data, and it is designed to integrate with the authentication and backend services already adopted by the PagoPA platform.

This implementation was inspired by and adapted from the work originally done in the `p4pa-superset` project. We thank the maintainers and contributors of that repository for the starting point.

## Purpose

- expose curated dashboards and analytics for pagoPA data;
- provide a Superset-based UI for business users and operators;
- integrate with platform authentication and domain services;
- run in a reproducible containerized environment.

## Architecture

The stack is composed of:

- Apache Superset as the analytics and dashboard layer;
- PostgreSQL as the metadata and application database;
- Redis as cache and Celery support;
- a custom Docker image built on top of the official Superset image.

## Dependencies

### Infrastructure services

- Redis
- PostgreSQL

## Configuration

For the full list of Superset options, refer to the official [Apache Superset installation and configuration documentation](https://github.com/apache/superset?tab=readme-ov-file#installation-and-configuration).

## Getting started

### Prerequisites

Install the following tools locally:

1. Docker
2. Docker Compose
3. An environment file with the required variables (for example, `.env`)

### Run with Docker Compose

From the repository root:

```bash
docker compose up --build
```

This starts:

- PostgreSQL
- Redis
- the Superset application on port `8088`

Access Superset at:

```text
http://localhost:8088
```

## References

- [Apache Superset](https://github.com/apache/superset)
- [p4pa-superset](https://github.com/pagopa/p4pa-superset)