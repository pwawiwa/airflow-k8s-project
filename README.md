# Airflow on Kubernetes (Playground)

This project demonstrates a simple Apache Airflow deployment on a local Kubernetes cluster (Docker Desktop).

## Understanding the Setup

### 1. The Executor: KubernetesExecutor
We use the **KubernetesExecutor**. Unlike the CeleryExecutor which requires a fixed set of workers, the KubernetesExecutor creates a **new Pod for each task instance**.
- **Pros**: Dynamic scaling, high resource efficiency (zero waste when idle), and isolation.
- **Cons**: Slightly higher overhead for short tasks (Pod startup time).

### 2. The Deployment: Helm
We use the official **Airflow Helm Chart**. It manages multiple components:
- **Webserver**: The UI you interact with.
- **Scheduler**: Monitoring DAGs and tasks, and triggering executions.
- **PostgreSQL**: Metadata database for Airflow.

### 3. DAG Syncing
In a real production environment, we use **Git-Sync**. This is a sidecar container that runs alongside the Scheduler and Webserver, continuously pulling the latest code from GitHub.
In this "Simple" setup, we use a **PersistentVolume (PV)** to store DAGs locally for ease of use, but the configuration for Git-Sync is ready in `values.yaml`.

## How to Deploy

1. Add the Airflow Helm repository:
   ```bash
   helm repo add apache-airflow https://airflow.apache.org
   helm repo update
   ```

2. Create the namespace:
   ```bash
   kubectl create namespace airflow
   ```

3. Install Airflow using the provided `values.yaml`:
   ```bash
   helm install airflow apache-airflow/airflow -n airflow -f values.yaml
   ```

4. Port-forward to access the UI:
   ```bash
   kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow
   ```
   > Default credentials: `admin` / `admin`

## GitHub Integration

1. Create a new repository on GitHub (already done).
2. Link this local repo:
   ```bash
   git remote add origin https://github.com/pwawiwa/airflow-k8s-project.git
   git add .
   git commit -m "Update URLs"
   git push
   ```
