# Arrbo — QA-Focused Data & API Reliability Project

![CI](https://github.com/josef-spradlin/Arrbo/actions/workflows/ci.yml/badge.svg)
![Dockerized](https://img.shields.io/badge/docker-ready-blue.svg)

**Arrbo** is a full-stack NBA analytics system built to showcase **Quality Assurance** practices in a realistic, production-style environment.

Although the domain is sports analytics, the engineering patterns are meant to reflect systems found in regulated industries like healthcare and finance.

---

## What This Project Demonstrates

This project emphasizes **system correctness**, **reliability**, and **automation** over feature development. It demonstrates how a QA professional can build testable, deterministic, and CI-ready systems.

### Data Quality & Integrity

- Deterministic database seeding (local and CI)
- Referential integrity and uniqueness checks
- Idempotent schema and seed migrations via Flyway

### API Reliability & Contract Testing

- Health-checked Spring Boot API
- Contract and smoke tests for:
  - Status codes
  - Response structure
  - Required fields
- CI fails fast on contract violations

### End-to-End System Validation

- Full-stack validation from database to frontend
- Headless UI tests against a preview frontend
- Performance smoke tests for regression detection

### Production-Style Tooling

- Docker Compose for local/CI parity
- GitHub Actions CI with isolated DB lifecycle
- One-command workflows via `run.py`

---

## High-Level Architecture

PostgreSQL

├── Flyway migrations (schema + seed data)

├── Python ingestion (ETL-style population)

Spring Boot API

├── REST endpoints

├── Health checks

└── Repository-based data access

Vue Frontend

└── Used for headless UI test validation


---

## Test Strategy

Tests are organized by type using `pytest` markers and run consistently across local and CI environments.

- `db`: Validates referential integrity, constraints, and uniqueness
- `api`: Ensures correct status codes, schema contracts, and required fields
- `perf`: Catches major performance regressions
- `ui`: Executes headless end-to-end UI tests against a preview frontend

---

## Project Structure

backend-springboot/ # Spring Boot API + Flyway migrations

ingestion-python/ # ETL-style ingestion and seeding

frontend-vue/ # Vue frontend

tests/

├── db/ # Database integrity tests

├── api/ # API contract & smoke tests

├── perf/ # Performance regression tests

└── ui/ # UI end-to-end tests

ci/

└── seed.sql # Deterministic seed data for CI

run.py # One command runner for all workflows


---

## Prerequisites

- Git
- Docker Desktop
- Python 3.11+
- Node.js (LTS)

---

## Quickstart

From the root directory:

Copy the environment template and create your runtime environment files:

`cp .env.example .env`

Create both `.env` and `.env.test` in the project root using values from `.env.example`.

Ensure Docker Desktop is running, then start the full application (database, API, and frontend):

`py run.py up`

To populate the system with current NBA game data (today and tomorrow):

`py run.py up --ingest`

To start with a completely fresh database:

`py run.py up --reset-db`

---

### Seed Static Data (Offseason / No Games)

If there are no games available, you can populate the application with deterministic seed data:

Seed without starting services:  
`py run.py seed`

Reset database and apply seed data:  
`py run.py seed --reset-db`

---

### Stop Services

Stop all running services:  
`py run.py down`

Stop services and wipe the database volume:  
`py run.py down --reset-db`

---

## Running Tests

Run the full test suite (database, API, performance, and UI):

`py run.py test`

Optional — reset the database before running tests:

`py run.py test --reset-db`

This command will:

- Start required services
- Wait for health checks
- Execute all test layers in order
- Run headless UI tests against a production-style frontend preview

---

## Why This Project Exists

Arrbo is designed to demonstrate the mindset and workflow of a QA Engineer:

- Enforces correctness at every service boundary
- Designs deterministic and repeatable testing pipelines
- Treats CI/CD as a first-class concern
- Surfaces and prevents failure modes before they reach production
