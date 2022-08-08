# https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-base
FROM public.ecr.aws/lambda/python:3.9

# AWS Lambda Insights agent
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights-Getting-Started-docker.html
# RUN curl -O https://lambda-insights-extension.s3-ap-northeast-1.amazonaws.com/amazon_linux/lambda-insights-extension.rpm && \
#     rpm -U lambda-insights-extension.rpm && \
#     rm -f lambda-insights-extension.rpm

# Not compatible with ARM64 ! Awaiting AWS Support answer to find a suitable RPM package for Graviton

# Install Poetry package manager
RUN POETRY_VERSION="1.1.12" curl -sSL https://install.python-poetry.org | python3 && rm -rf ~/.cache
ENV PATH="~/.local/bin:$PATH"

# Install dependencies via Poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev && rm -rf ~/.cache/

# Copy source code
COPY api/ api/

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD ["api.lambda_function.lambda_handler"]