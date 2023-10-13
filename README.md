# ZenGen Application

ZenGen is a full-stack web application that generates Zen Koans and associates imagery using GPT-4 and DALL-E.

## Features

- User can input a prompt to generate a Zen Koan.
- Displays generated Koan and an associated image.
- Saves all generated Koans and images.
- Display a random selection of 10 generated Koans on the homepage.

## Getting Started

### Prerequisites
- Docker

### Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/zengen-app.git
```

2. Build and run the Docker container:

```bash
docker build -t zengen-app .
docker run -p 5000:5000 zengen-app
```

Now, the application should be running at http://localhost:5000.
