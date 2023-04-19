# 介绍 Kubernetes

Kubernetes 是一个开源的容器编排平台，可以帮助开发者和运维人员更高效地部署、管理和扩展容器化应用程序。

## 什么是容器

容器是一种轻量级的虚拟化技术，可以将应用程序及其依赖项打包为一个可移植的镜像，然后在不同的计算环境中运行。

## 为什么需要 Kubernetes

随着容器化应用程序的普及，管理大规模容器集群变得越来越复杂。Kubernetes 可以帮助用户自动化部署、扩展和管理容器化应用程序，从而提高开发效率、简化操作流程、提高可靠性和可伸缩性。

## Kubernetes 的核心概念

Kubernetes 中有几个核心概念，包括：

- Pod：最小部署单元，包含一个或多个容器。
- ReplicaSet：用于定义 Pod 的副本数量和更新策略。
- Deployment：管理 ReplicaSet 和 Pod 的更新和滚动更新。
- Service：提供网络访问和负载均衡。
- Namespace：用于将资源隔离在不同的逻辑分区中。

## Kubernetes 的架构

Kubernetes 采用了一个分层的架构，包括：

- 控制平面：用于管理集群状态的组件，包括 API Server、Controller Manager、Scheduler 等。
- 数据平面：用于运行容器的节点，包括 Node、kubelet、Container Runtime 等。
- 存储层：用于存储集群状态和应用程序数据的存储系统。

## Kubernetes 的优势

Kubernetes 提供了很多优势，包括：

- 可移植性：支持在不同的云服务提供商和本地数据中心中运行。
- 可伸缩性：可以自动扩展和缩小容器数量以满足负载需求。
- 可靠性：提供自动恢复和自动故障转移功能，确保应用程序高可用性。
- 安全性：提供多种安全功能，包括身份验证、授权、加密等。


## Deploying a Python Flask Project on Kubernetes

This guide will walk you through the process of deploying a Python Flask project on Kubernetes and exposing its API.

### Prerequisites

- A Python Flask project
- Docker installed on your local machine
- A Kubernetes cluster (e.g., Minikube, kubeadm, or a managed Kubernetes service like GKE or EKS)
- kubectl command-line tool installed and configured to interact with your cluster

### Step 0: Create a simple flask project
```python
import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return f'Hello from pod {os.environ.get("POD_NAME")}!'
```
### Step 1: Create a Dockerfile

Create a `Dockerfile` in your Flask project's root directory with the following contents:

```Dockerfile
FROM python:3.8-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8001

CMD ["gunicorn", "-b", "0.0.0.0:8001", "app:app"]
```

This Dockerfile specifies the base image, sets up a working directory, installs the required packages, copies the project files, exposes port 5000, and starts the application using Gunicorn.

### Step 2: [Option 1] Build and push the Docker Image to a Registry


Run the following command in your project's root directory to build the Docker image:

```sh
docker build -t project-k .
```

Push the Docker image to a container registry like Docker Hub or Google Container Registry. For example, to push the image to Docker Hub:

1. Log in to Docker Hub:

```sh
docker login
```

2. Tag the image:

```sh
docker tag your-image-name your-dockerhub-username/your-image-name
```

3. Push the image:

```sh
docker push your-dockerhub-username/your-image-name
```
### Step 2: [Option 2] Build and push with Github Actions

Fork this repo to your personal github account.

### Step 3: Create a Kubernetes Deployment

Create a file named `deployment.yaml` with the following contents:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: project-k-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: project-k
  template:
    metadata:
      labels:
        app: project-k
    spec:
      containers:
      - name: project-k
        image: ghcr.io/randomstar/project-k:main
        ports:
        - containerPort: 8001
        resources:
          limits:
            cpu: "0.1"
            memory: 128Mi

```

Replace `your-dockerhub-username/your-image-name` with the appropriate Docker image name.

### Step 4: Create a Kubernetes Service

Create a file named `service.yaml` with the following contents:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: project-k-service
spec:
  selector:
    app: project-k
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8001
  type: LoadBalancer
```

This file defines a LoadBalancer service that exposes the Flask app on port 80.

### Step 5: Deploy the Application

Apply the deployment and service configurations using kubectl:

```sh
kubectl apply -f flask-deployment.yaml
kubectl apply -f flask-service.yaml
```

### Step 6: Access the Flask API

Get the external IP address of the LoadBalancer service:

```sh
kubectl get services
```

Once the external IP is available, you can access the Flask API using the external IP and port 80