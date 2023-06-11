# NLP Boilerplate Project

Welcome to the NLP Boilerplate project

This is a Python-based boilerplate project for Natural Language Processing (NLP) tasks. It comes pre-configured with essential components that can be useful for starting a NLP project.

## Features

- **FastAPI:** REST API using FastAPI (high-performance web framework for building APIs in Python) - user authentication and authorization (JWT - JSON Web Token).

- **Postgres:** relational data storage.

- **Elasticsearch:** distributed search and analytics engine, to store and retrieve textual data efficiently.

- **Redis Caching:** caching, a fast in-memory data store - improve the performance of your NLP application.

- **Docker / Docker Compose:** container applications using Docker and Docker Compose with hot reloading for faster development cycles - simplify the development and deployment processes.

## Getting Started

Follow the instructions below to get the NLP API Boilerplate project up and running on your local machine.

### Prerequisites

Make sure you have the following software installed:

- Python >= 3.9
- Docker
- Docker Compose

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/hugohonda/nlp-api-boilerplate
   cd nlp-api-boilerplate
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

- Rename the `.env.example` file to `.env` and update the configuration variables as per your needs.

  ```bash
  cp .env.example .env
  ```

<!-- 2. Modify the `config.py` file to customize the application settings and configurations. -->

### Running the Application

To start the NLP Boilerplate application, follow these steps:

1. Using Docker Compose (recommended):

   ```bash
   docker-compose up --build
   ```

   This command will build and start the Docker containers for the application and its dependencies.

2. Alternatively, you can run the application directly:

   ```bash
   uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8989 --reload --forwarded-allow-ips '*'
   ```

   This command will start the application without Docker, but make sure to set up the required services (PostgreSQL, Elasticsearch, and Redis) separately.

## Usage

Once the application is up and running, you can access it by visiting `http://localhost:8989` in your web browser.

### API Documentation

The API documentation is available at `http://localhost:8989/docs`, providing details about the available endpoints and their usage.

- [FastAPI](https://fastapi.tiangolo.com)
- [PostgreSQL](https://www.postgresql.org)
- [Elasticsearch](https://www.elastic.co/guide/index.html)
- [Redis](https://redis.io/docs/getting-started/installation/)
- [Docker](https://docs.docker.com/desktop/)
- [Docker Compose](https://docs.docker.com/compose/)

## Contact

For any questions or inquiries, please contact at

honda . data . science at gmail . com
