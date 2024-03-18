# Use an official Python runtime as a parent image
FROM python:3

# Set environment variable to prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Set environment variable to not buffer Python output (print statements)
ENV PYTHONUNBUFFERED 1

# Set the working directory to /
WORKDIR /app

# Copy the current directory contents into the container at /
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 8000 for the Django application
EXPOSE 8000

# Command to run the application
CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]
