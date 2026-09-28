# Project 2 - DevOps Monitoring & Observability Platform

A containerized monitoring and observability platform built with Python, Flask, Docker, Docker Compose, Prometheus, Grafana, and Node Exporter.

The project demonstrates how application metrics can be exposed from a Flask API, collected by Prometheus, and visualized through a Grafana monitoring dashboard.

## Project Overview

This project was built to practice real-world DevOps monitoring and observability concepts.

The platform contains:

- Flask API running with Gunicorn
- Prometheus for metrics collection
- Grafana for metrics visualization
- Node Exporter for system and runtime metrics
- Docker and Docker Compose for container orchestration
- A saved Grafana monitoring dashboard
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
                               | PromQL
                               v
                    +---------------------+
                    |       Grafana       |
                    |       :3000         |
                    | Monitoring Dashboard|
                    +---------------------+

                    +---------------------+
                    |    Node Exporter    |
                    |       :9100         |
                    +----------+----------+
                               |
                               v
                         Prometheus