# Use a minimal base image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy only the necessary files to the container
COPY ./app /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the FastAPI app will run
EXPOSE 8000

# Command to run the application
#CMD ["uvicorn", "app.main:app", "--port", "8000", "--reload", "--log-level", "debug"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# Command to keep the container running
#CMD ["tail", "-f", "/dev/null"]