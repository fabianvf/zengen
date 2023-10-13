# Build the React Frontend
FROM node:16 AS build
WORKDIR /usr/src/app
COPY package*.json ./
COPY public ./public
COPY src ./src
RUN npm install
RUN npm run build

# Setup the Python Backend
FROM python:3.8
WORKDIR /usr/src/app

COPY server/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY server ./
COPY --from=build /usr/src/app/build /usr/src/app/frontend/build
ENV STATIC_FOLDER=/usr/src/app/frontend/build

RUN groupadd -r zengen \
 && useradd --no-log-init -d /usr/src/app -r -g zengen zengen \
 && chown -R zengen:zengen /usr/src/app

USER zengen
# Command to run the application
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-"]