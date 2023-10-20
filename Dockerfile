# Build the React Frontend
FROM node:16 AS build
WORKDIR /usr/src/app
COPY package*.json ./
COPY public ./public
COPY src ./src
RUN npm install
RUN npm run build

# Setup the Python Backend
FROM python:3.10
WORKDIR /usr/src/app

COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY server ./
# Just in case there's a local db sitting in here
RUN rm -rf ./instance || true
COPY --from=build /usr/src/app/build /usr/src/app/frontend
ENV STATIC_FOLDER=/usr/src/app/frontend/static
# Ensure the koans image directory is present
RUN mkdir -p /usr/src/app/frontend/static/koans

RUN groupadd -r zengen \
 && useradd --no-log-init -d /usr/src/app -r -g 0 zengen \
 && chown -R zengen:zengen /usr/src/app \
 && mkdir -p /usr/src/app/instance && chmod +777 /usr/src/app/instance \
 && mkdir -p /usr/src/app/frontend/static/koans chmod +777 /usr/src/app/frontend/static/koans

USER zengen
# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
