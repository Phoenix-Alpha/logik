# https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-base
FROM public.ecr.aws/lambda/python:3.9

# Install dependencies
RUN pip install --upgrade pip wheel --no-cache-dir
COPY requirements.txt .
RUN pip install --requirement requirements.txt --no-cache-dir

# Copy source code
COPY lambda_function.py .

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["lambda_function.lambda_handler"]