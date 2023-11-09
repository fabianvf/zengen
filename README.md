# ZenGen Application

ZenGen is a full-stack web application that generates Zen Koans and associates imagery using GPT-4 and DALL-E.
Loosely inspired by Ummon from the book series _The Hyperion Cantos_.

It was written largely by ChatGPT with my supervision. The initial conversation can be viewed here:

https://chat.openai.com/share/c8158113-b979-4639-95d8-95150f841484

## Features

- User can input a prompt to generate a Zen Koan.
- Displays generated Koan and an associated image.
- Saves all generated Koans and images.
- Display a random selection of 10 generated Koans on the homepage.

## Getting Started

### Prerequisites
- Docker

### Setup

2. Build and run the Docker container:

```bash
docker build -t zengen-app .
docker run -p -e OPENAI_API_KEY='sk-<your-api-key>' 5000:5000 zengen-app
```

Now, the application should be running at http://localhost:5000.

### Deployment to Kubernetes

Deployment manifests are provided for deploying ZenGen on a Kubernetes cluster, located in the [deploy](https://github.com/fabianvf/zengen/tree/main/deploy) directory. Here's a brief overview:

- `zengen.yaml`: Deployment, service, and pvc manifest for the ZenGen app.
- `postgres.yaml`: Deployment, service, and pvc manifest for the PostgreSQL database.
- ...

Ensure to customize the manifests, particularly the environment variables and persistent volume claims, to match your environment before deploying.

### Configuration

ZenGen can be configured via environment variables, defined in [server/settings.py](https://github.com/fabianvf/zengen/blob/main/server/settings.py). Here are the key variables:

- `DATABASE_URL`: The URL of the database to connect to.
- `OPENAI_API_KEY`: Your OpenAI API key for GPT 4 and DALL-E 3.
