# Sensor App Django Vue

This project consists of a Django backend and a Vue.js frontend. It can be run using Docker containers or using traditional development environments.

## Table of Contents

- [Docker Setup](#docker-setup)
  - [Build and Run with Docker](#build-and-run-with-docker)
  - [Troubleshooting Docker](#troubleshooting-docker)
- [Local Development Setup](#local-development-setup)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)

## Docker Setup

### Build and Run with Docker

To build and run the project using Docker, follow these steps:

1. **Navigate to the root folder of the project**:

    ```bash
    cd path/to/sensor_app_django_vue
    ```

2. **Ensure Docker and Docker Compose are installed**:

    Check Docker version:

    ```bash
    docker --version
    ```

    Check Docker Compose version:

    ```bash
    docker-compose --version
    ```

3. **Build and start the containers**:

    Use the following command to build the Docker images and start the containers:

    ```bash
    docker-compose up --build
    ```

    This command will:
    - Build the Docker images for the backend and frontend.
    - Start the containers and set up the services defined in the `docker-compose.yml` file.

4. **Access the applications**:

    - Backend: [http://localhost:8000](http://localhost:8000)
    - Frontend: [http://localhost:8080](http://localhost:8080) (or the port you have specified in the `docker-compose.yml`)

### Troubleshooting Docker

If you encounter issues with Docker, such as the Docker daemon not running or WSL errors, follow these steps:

1. **Ensure WSL 2 is installed and set up properly**:
   - Open PowerShell and run:

     ```bash
     wsl --list --verbose
     ```

   - If WSL 2 is not set up, follow instructions from the [Microsoft documentation](https://aka.ms/wsl2-install) to enable virtualization and install WSL 2.

2. **Restart Docker Desktop**:
   - Sometimes a restart of Docker Desktop can resolve issues.

3. **Check Docker service status**:
   - Ensure the Docker service is running.

## Local Development Setup

### Backend Setup

If you prefer to run the backend without Docker, follow these steps:

1. **Set up a virtual environment**:

    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment**:

    On Windows:

    ```bash
    venv\Scripts\activate
    ```

    On macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Django development server**:

    ```bash
    python manage.py runserver
    ```

### Frontend Setup

To run the Vue.js frontend locally:

1. **Navigate to the frontend directory**:

    ```bash
    cd sensor_frontend
    ```

2. **Install dependencies**:

    ```bash
    npm install
    ```

3. **Run the development server**:

    ```bash
    npm run dev
    ```

4. **Access the frontend**:

    Open [http://localhost:8080](http://localhost:8080) (or the port you have configured) in your web browser.

## .gitignore

Make sure to add the following to your `.gitignore` file to prevent committing unnecessary files:

```plaintext
venv/
node_modules/
