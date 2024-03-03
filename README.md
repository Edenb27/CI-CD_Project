# CI/CD Project

## Background

In this project you will design and implement CI/CD pipelines for the Object Detection Service, to automate the deployment process for development and production environments. 

## Infrastructure

Since your service will be deployed in both **development** and **production** environments, you have to provision infrastructure for both envs:

- 2 telegram tokens - for dev and prod bots.
- Separate resources in AWS for dev and prod: S3, SQS, DynamoDB, Secret Manager, etc... 
- Both dev and prod services would be deployed **in the same** K8S cluster (in different namespaces).

## CI server

Use the Jenkins server we've setup in class, or create a new one if needed (either in k8s, EC2, or any other way). 
The below guidelines are related to Jenkins, but you can also use any other CI platform (e.g. GitHub Actions, Azure DevOps).  

- In your Jenkins server, create `dev` and `prod` folders (**New Item** -> **Folder**). Production related pipelines and credentials would be created in `prod` folder, similarly, development related pipelines are in `dev` folder.  
- All pipelines should be running on a containerized agent (the same Docker image for all pipelines). Use the `Dockerfile` we've presented in class as a baseline. 
- **No need** to run agents on different nodes! All pipelines can be running on the Jenkins server itself.

## Build pipelines

Design and implement build pipelines for the `polybot` and `yolo5` services:

- You can simply create 4 `Jenkinsfile`s as detailed below. Alternatively, if you want to reduce code duplication, use Jenkins [shared library](https://www.jenkins.io/doc/book/pipeline/shared-libraries/).

```text
.
├── yolo5-build-prod.Jenkinsfile
├── yolo5-build-dev.Jenkinsfile
├── polybot-build-prod.Jenkinsfile
├── polybot-build-dev.Jenkinsfile
```

- Both production and development pipelines should be triggered automatically upon push event.
- Make sure to build only services that their source code have been changed. If you changed the `polybot` code and pushed it, only the build pipeline of the `polybot` should be triggered. 
- Each new built Docker image should have a different image tag.
- Build pipeline for development environment should be triggered upon changes in branch `dev`.
- Build pipeline for production environment should be triggered upon changes in branch `main`.

## Deployment to Kubernetes using ArgoCD

[ArgoCD](https://argo-cd.readthedocs.io/en/stable/) is a declarative continuous delivery tool for Kubernetes. 

Argo automatically detects changes done in YAML manifests in your GitHub repo, and sync the cluster accordingly.
For example, if you change an image tag in a YAML manifest, and **commit and push** it, Argo can automatically deploy the new version into your cluster (instead of executing the `kubectl apply` command).
This pattern is called **GitOps**, which means, using Git repositories as the **source of truth** for defining the desired application state.

- In your K8S cluster, create `dev` and `prod` namespaces. 
- In your project repo, create YAML manifests for both development and production environments. For example:

  ```text
  .
  ├── k8s
  │   ├── dev
  │   │   ├── yolo5.yaml
  │   │   └── polybot.yaml
  │   └── prod
  │       ├── yolo5.yaml
  │       └── polybot.yaml
  ```

   - This is only a suggestion. Feel free to change to any other files layout that works for you.
   - You can use **Helm** if you want to reduce code duplications.

- Install Argo in your cluster by: 

  ```bash
  kubectl create namespace argocd
  kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
  ```
  
  You can access the server by port-forwarding the `argocd-server` service in `argocd` namespace.

- Create the below "release" pipelines that are triggered after a successful running of the build pipeline:

  ```text
  .
  ├── releases-dev.Jenkinsfile
  ├── releases-prod.Jenkinsfile
  ```
  
  - The release pipeline receives the new image tag from the build pipeline (similarly as done in class).
  - The pipelines will **commit and push** the new version of your YAML manifests to the `releases` branch of your Git repository. Once the new version of the YAML manifests is pushed, ArgoCD automatically detects the changes and initiates the deployment process.

- In your Argo server, create a new application (**+ New App**) for the `polybot` and `yolo5` for both development and production envs: 
  - The apps should use the `releases` branch as a source for YAML manifests.
  - Deployment to `dev` namespace should be done automatically.
  - Deployment to `prod` should be done manually using the **Sync** button in Argo.

## Pull Request testing pipelines (optional)

- Protect branch `main` so changes can be merged via a PR only.
- Create PR testing pipeline in Jenkins (only for prod, no need to test dev deployments):
  ```text
  .
  ├── pr-testing.Jenkinsfile
  ```

- In the pipeline, implement some test, it could be some unittest, a linting check, or any other minimal test.
- Make sure PR merging is blocked when the PR testing pipeline is failed.  


## Trying it all together 

1. From `main` branch, create a feature branch.
2. Commit some changes.
3. Merge your feature branch into `dev`, push, wait for Argo to deploy the change to development bot.
4. Create a PR from your feature branch into `main`, make sure you pass the PR testing pipeline.
5. Merge the PR. After a new version is ready to be released, deploy it manually to production bot. 

# Good Luck
