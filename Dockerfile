FROM python:3.9

# Install the AWS CLI to fetch credentials from ECS metadata
RUN apt-get update && apt-get install -y awscli

WORKDIR /python

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /src/main/python/app.py .

# Set AWS credentials or IAM role within the container
ENV AWS_ACCESS_KEY_ID=AKIARZSHOXKIXMUJYZ47
ENV AWS_SECRET_ACCESS_KEY=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
ENV AWS_DEFAULT_REGION=ap-south-1

CMD ["python", "app.py"]
