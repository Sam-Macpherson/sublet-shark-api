# Use official python 3.8 base image
FROM python:3.8-alpine

# Set working directory
WORKDIR /usr/src/subletshark

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install psycopg2 and Pillow dependencies
RUN apk update && \
    apk add postgresql-dev zlib-dev jpeg-dev gcc python3-dev musl-dev

# Install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy scripts/entrypoint.sh
COPY ./scripts/entrypoint.sh ./scripts/

# Copy project
COPY . .

# Run the entry point
ENTRYPOINT ["/usr/src/subletshark/scripts/entrypoint.sh"]
