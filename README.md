# Sensor App Django Vue

This project consists of a Django backend and a Vue.js frontend. It can be run using Docker containers or using traditional development environments.

## Table of Contents

- [Docker Setup](#docker-setup)
  - [Build and Run with Docker](#build-and-run-with-docker)
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

## Local Development Setup

### Backend Setup

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

