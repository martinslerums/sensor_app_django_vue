# Overview

SAF Sensor App is a web application with a Vue.js frontend and a Django backend. This guide provides instructions on how to set up and run the project using Docker and also provides alternative setup instructions for running the project directly with npm and python.

# Project Structure

sensor_backend/: Contains the Django backend code.
sensor_frontend/: Contains the Vue.js frontend code.
docker-compose.yml: Docker Compose configuration for running the backend and frontend together.

## Docker-Based Setup

## Prerequisites

Docker and Docker Compose should be installed on your machine.

## Build and Run

      1. Navigate to the Project Root Directory
        Open a terminal and navigate to the root of your project where docker-compose.yml is located

      2. Build and Start Containers

        ```bash
          docker-compose up --build
        ```

      3.Access the Application

        Once the containers are running, you can access:
        Frontend: http://localhost:8080
        Backend API: http://localhost:8000

      4.Stopping the Containers

        ```bash
          docker-compose down
        ```

## Traditional Setup

## Backend Setup

    1. Navigate to the Backend Directory

        ```bash
          cd path/to/your/project/sensor_backend
        ```

    2. Create and Activate a Virtual Environment

        ```bash
          python -m venv venv
          source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
        ```

    3. Install Dependencies

        ```bash
          pip install -r requirements.txt
        ```

    4. Run the Django Server

        ```bash
          python manage.py runserver
        ```

    The backend will be available at http://127.0.0.1:8000.

## Frontend Setup

    1. Navigate to the Frontend Directory

        ```bash
          cd path/to/your/project/sensor_frontend
        ```

    2. Install Node.js Dependencies

        ```bash
          npm install
        ```

    3. Run the Development Server

        ```bash
          npm run dev
        ```