# Use the official lightweight Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /python

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY /src/main/python/app.py .

# Define environment variables
# ENV AWS_ACCESS_KEY_ID=AKIARZSHOXKIXMUJYZ47
# ENV AWS_SECRET_ACCESS_KEY=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
# ENV AWS_DEFAULT_REGION=ap-south-1

CMD ["python", "app.py"]
