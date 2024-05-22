# Documentation for GitHub Actions Workflows

## Table of Contents

- [Documentation for GitHub Actions Workflows](#documentation-for-github-actions-workflows)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Setup and Configuration](#setup-and-configuration)
  - [CI Workflow](#ci-workflow)
    - [Triggers](#triggers)
    - [Jobs and Steps](#jobs-and-steps)
  - [CD Workflow](#cd-workflow)
    - [Triggers](#triggers-1)
    - [Jobs and Steps](#jobs-and-steps-1)

## Introduction

This documentation provides a comprehensive guide to the CI/CD workflows configured for the Django application using GitHub Actions. It covers all steps, tasks, triggers, installation, configuration, and testing procedures.

## Setup and Configuration

Before using the workflows, ensure you have the necessary secrets set up in your GitHub repository. The required secrets are:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_PASSWORD`
- `AZURE_CREDENTIALS`
- `SUBSCRIPTION_ID`
- `RESOURCE_GROUP`
- `RESSOURCE_GROUP`
- `WORKSPACE_NAME`
- `SERVER`
- `DATABASE`
- `POSTGRES_USER`
- `PASSWORD`
- `SECRET_KEY`

To add these secrets:

1. Navigate to your GitHub repository.
2. Go to **Settings** > **Secrets and variables** > **Actions**.
3. Click on **New repository secret**.
4. Add each secret with the appropriate values.

## CI Workflow

### Triggers

The CI workflow is triggered on every push to the repository.


### Jobs and Steps

Job: Health Check
This job ensures the code quality and correctness through unittesting, code formatting checks and code security check

## CD Workflow
### Triggers
The CD workflow is triggered on pushes and pull requests to the main branch for specific paths.

paths:
    - 'api/**'
    - '.github/workflows/cd.yaml'

### Jobs and Steps
Job: Build and Deploy
This job builds a Docker image, pushes it to Docker Hub, and deploys it to Azure Container Instance.