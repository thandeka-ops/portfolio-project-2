# Project 2 - DevOps Monitoring & Observability Platform

A containerized monitoring and observability platform built with Python, Flask, Docker, Docker Compose, Prometheus, Grafana, and Node Exporter.

The project demonstrates how application metrics can be exposed from a Flask API, collected by Prometheus, visualized through Grafana, and monitored using Prometheus alerting rules.

## Project Overview

This project was built to practice real-world DevOps monitoring, observability, and alerting concepts.

The platform contains:

- Flask API running with Gunicorn
- Prometheus for metrics collection and alerting
- Grafana for metrics visualization
- Node Exporter for system and runtime metrics
- Docker and Docker Compose for container orchestration
- A saved Grafana monitoring dashboard
- Prometheus alerting rules
- Environment variables for Grafana credentials

The Flask application automatically exposes Prometheus-compatible metrics through the `/metrics` endpoint.

## Architecture

```text
                    +---------------------+
                    |      Flask API      |
                    |      Gunicorn       |
                    |       :5000         |
                    +----------+----------+
                               |
                               | /metrics
                               v
                    +---------------------+
                    |     Prometheus      |
                    |       :9090         |
                    +----------+----------+
                               |
                 +-------------+-------------+
                 |                           |
                 | PromQL                    | Alert Rules
                 v                           v
        +---------------------+       +----------------------+
        |       Grafana       |       | Prometheus Alerts    |
        |       :3000         |       |                      |
        | Monitoring Dashboard|       | FlaskAPIDown         |
        +---------------------+       | HighHTTPErrorRate    |
                                      | HighAPIResponseTime  |
                                      +----------------------+

                    +---------------------+
                    |    Node Exporter    |
                    |       :9100         |
                    +----------+----------+
                               |
                               v
                         Prometheus
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Application runtime |
| Flask | REST API |
| Gunicorn | Production WSGI server |
| prometheus_flask_exporter | Flask Prometheus metrics |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| Prometheus | Metrics collection, querying, and alerting |
| Grafana | Monitoring dashboards and visualization |
| Node Exporter | System and runtime metrics |
| YAML | Docker Compose, Prometheus, and alert configuration |
| Git and GitHub | Version control |

## Project Structure

```text
portfolio-project-2/
|
+-- .gitignore
+-- Dockerfile
+-- README.md
+-- docker-compose.yml
|
+-- app/
|   +-- __init__.py
|   +-- app.py
|   +-- requirements.txt
|
+-- grafana/
|   +-- dashboard.json
|
+-- prometheus/
    +-- alerts.yml
    +-- prometheus.yml
```

## Flask API

The application provides the following endpoints.

### Home

```text
GET /
```

Returns application information including the application name, environment, version, and status.

Example:

```json
{
  "application": "Enterprise Monitoring Platform",
  "environment": "Development",
  "version": "2.0.0",
  "status": "Running Successfully"
}
```

### Health Check

```text
GET /health
```

Returns:

```json
{
  "status": "healthy"
}
```

### Version

```text
GET /version
```

Returns:

```json
{
  "version": "2.0.0"
}
```

### Metrics

```text
GET /metrics
```

The `/metrics` endpoint is automatically provided by `prometheus_flask_exporter`.

These metrics are collected by Prometheus and used by Grafana for visualization and alert evaluation.

## Prometheus Configuration

Prometheus uses a 5-second scrape interval.

It collects metrics from:

```text
prometheus:9090
flask-api:5000/metrics
node-exporter:9100
```

The Flask application is configured as a Prometheus scrape target using:

```yaml
metrics_path: /metrics
```

Prometheus also loads the alerting rules from:

```text
/etc/prometheus/alerts.yml
```

## Prometheus Alerting

The project includes three Prometheus alerting rules.

The rules are stored in:

```text
prometheus/alerts.yml
```

### FlaskAPIDown

Detects when the Flask API is unavailable.

```yaml
expr: up{job="flask-api"} == 0
```

The alert fires after the Flask API has been unavailable for 30 seconds.

Severity:

```text
critical
```

### HighHTTPErrorRate

Detects when more than 5% of HTTP requests are returning 5xx errors.

Severity:

```text
warning
```

### HighAPIResponseTime

Detects when the 95th percentile API response time exceeds 1 second for 2 minutes.

Severity:

```text
warning
```

## Alert Testing

The alerting functionality was tested manually.

The Flask API was intentionally stopped while Prometheus continued running.

The result was:

```text
FlaskAPIDown -> FIRING
```

After the Flask API was started again:

```text
FlaskAPIDown -> INACTIVE
```

This verified the complete alert lifecycle:

```text
API healthy
    |
    v
Alert INACTIVE
    |
    v
API stopped
    |
    v
Prometheus detects failure
    |
    v
FlaskAPIDown -> FIRING
    |
    v
API restored
    |
    v
FlaskAPIDown -> INACTIVE
```

The alert rules were also validated using Prometheus `promtool`:

```text
SUCCESS: 3 rules found
```

## Grafana Dashboard

Grafana provides the visualization layer for the monitoring platform.

The repository contains the saved dashboard:

```text
grafana/dashboard.json
```

The dashboard displays metrics collected by Prometheus, including application request metrics and system/runtime information.

The dashboard was connected to the Prometheus data source and verified to display live monitoring data.

## Docker Compose Services

Docker Compose runs the monitoring platform as four services.

### Flask API

```text
Port: 5000
```

### Prometheus

```text
Port: 9090
```

### Grafana

```text
Port: 3000
```

### Node Exporter

```text
Port: 9100
```

Check the services with:

```bash
docker compose ps
```

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/thandeka-ops/portfolio-project-2.git
cd portfolio-project-2
```

### 2. Create the environment file

Create a `.env` file in the project root:

```env
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=your_secure_password
```

Use your own secure password.

Do not commit the `.env` file to Git.

The repository `.gitignore` excludes `.env`.

### 3. Start the platform

```bash
docker compose up -d
```

### 4. Verify the containers

```bash
docker compose ps
```

Expected services:

```text
portfolio-project-2-api
portfolio-project-2-prometheus
portfolio-project-2-grafana
portfolio-project-2-node-exporter
```

## Accessing the Services

### Flask API

```text
http://localhost:5000
```

Health check:

```text
http://localhost:5000/health
```

Metrics:

```text
http://localhost:5000/metrics
```

### Prometheus

```text
http://localhost:9090
```

Prometheus targets:

```text
http://localhost:9090/targets
```

Prometheus alerts:

```text
http://localhost:9090/alerts
```

### Grafana

```text
http://localhost:3000
```

Use the Grafana credentials defined in the local `.env` file.

## Monitoring Workflow

```text
1. Flask receives HTTP requests
        |
        v
2. prometheus_flask_exporter exposes metrics
        |
        v
3. Prometheus scrapes /metrics
        |
        v
4. Prometheus stores the metrics
        |
        +----------------------+
        |                      |
        v                      v
   Grafana Dashboard      Alert Rules
        |                      |
        v                      v
   Visualization          Detection
```

## Verification

The platform was tested by verifying the following.

### Docker Compose configuration

```bash
docker compose config --quiet
```

### Running containers

```bash
docker compose ps
```

### Flask API

```bash
curl http://localhost:5000/
```

### Health endpoint

```bash
curl http://localhost:5000/health
```

### Prometheus metrics

```bash
curl http://localhost:5000/metrics
```

### Prometheus targets

The Prometheus targets page was verified to show the configured monitoring targets as available.

### Prometheus alert rules

The alert rules were validated with:

```bash
promtool check rules /etc/prometheus/alerts.yml
```

The validation returned:

```text
SUCCESS: 3 rules found
```

### Alert lifecycle

The `FlaskAPIDown` alert was tested by stopping the Flask API and verifying that the alert entered the `FIRING` state.

The API was then restored and the alert returned to `INACTIVE`.

### Grafana

The Grafana dashboard was verified to display application and system monitoring metrics collected by Prometheus.

## Security

Grafana credentials are provided through environment variables:

```yaml
environment:
  GF_SECURITY_ADMIN_USER: ${GRAFANA_ADMIN_USER}
  GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD}
```

The `.env` file is excluded from Git using `.gitignore`.

Passwords should never be stored directly in `docker-compose.yml` or committed to the repository.

## DevOps Skills Demonstrated

This project demonstrates practical experience with:

- Python and Flask
- Docker
- Docker Compose
- Prometheus
- Grafana
- Node Exporter
- Metrics collection
- PromQL monitoring
- Prometheus alerting
- Alert rule configuration
- Alert testing and recovery verification
- Application observability
- Health checks
- Environment-variable configuration
- Git and GitHub
- YAML configuration
- Gunicorn deployment
- Monitoring dashboard development
- Troubleshooting containerized monitoring systems

## What I Learned

Through this project I practiced:

- Instrumenting a Flask application for observability
- Exposing application metrics
- Configuring Prometheus scrape targets
- Building a multi-container monitoring stack
- Connecting Grafana to Prometheus
- Restoring and using Grafana dashboards
- Creating Prometheus alerting rules
- Validating Prometheus alert rules
- Testing alert conditions
- Verifying alert recovery
- Using environment variables for application configuration
- Troubleshooting Docker Compose configuration issues
- Validating monitoring data with Prometheus
- Visualizing application and system metrics in Grafana

## Future Improvements

Future improvements include:

- Grafana notification channels
- More advanced alerting rules
- Persistent Prometheus storage
- Persistent Grafana configuration
- Centralized logging
- Container health checks
- CI/CD automation
- AWS deployment
- Infrastructure as Code
- Kubernetes deployment

## Author

**Tholiwe Mchunu**

Junior DevOps & Cloud Engineer  
KwaZulu-Natal, South Africa

GitHub:

https://github.com/thandeka-ops

## Project Status

**Status: Monitoring and alerting platform completed**

The core monitoring platform is operational locally with Flask, Prometheus, Grafana, Node Exporter, and Docker Compose.

Prometheus alerting has been implemented and tested by intentionally stopping the Flask API, verifying that the `FlaskAPIDown` alert entered the `FIRING` state, restoring the API, and verifying that the alert returned to `INACTIVE`.