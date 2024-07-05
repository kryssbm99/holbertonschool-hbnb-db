FROM python:3.11-alpine

# Set environment variables to prevent Python from writing .pyc files to disk
# and to ensure that Python output is sent straight to terminal (without buffering)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create the data directory in the user's directory
RUN mkdir holbertonschool-hbnb-db

# Copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# Upgrade pip and install the required Python packages
RUN pip install --upgrade pip \
    && pip install -r /app/requirements.txt

# Install system dependencies
RUN apk update \
    && apk add --no-cache --virtual .build-deps gcc musl-dev \
    && apk add --no-cache postgresql-dev

# Copy the entire project into the image and set the working directory
COPY . /app
WORKDIR /app

# Define environment variable for the port
ENV PORT 5002

# Expose the port the app runs on
EXPOSE 5002

# Run the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5002", "hbnb:app"]
