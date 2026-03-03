# 1. Use NVIDIA CUDA base
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# 2. Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# 3. Install build dependencies
RUN apt-get update && apt-get install -y \
    wget build-essential libssl-dev zlib1g-dev \
    libncurses5-dev libgdbm-dev libnss3-dev \
    libsqlite3-dev libreadline-dev libffi-dev \
    curl libbz2-dev git \
    && rm -rf /var/lib/apt/lists/*

# 4. Download, Compile, and Install Python 3.12.10
RUN wget https://www.python.org/ftp/python/3.12.10/Python-3.12.10.tgz \
    && tar -xf Python-3.12.10.tgz \
    && cd Python-3.12.10 \
    && ./configure --enable-optimizations --with-ensurepip=install \
    && make -j$(nproc) \
    && make altinstall \
    # Link the newly built python to the standard paths
    && ln -sf /usr/local/bin/python3.12 /usr/bin/python3 \
    && ln -sf /usr/local/bin/python3.12 /usr/bin/python \
    && cd .. && rm -rf Python-3.12.10*

# 5. Install Poetry (pointing directly to our new python)
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# 6. Copy ONLY dependency files for better caching
COPY pyproject.toml poetry.lock* ./

# 7. Install dependencies (Disabling venv since Docker is already isolated)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# 8. Copy the rest of the project
COPY . .

# 9. Default command to start training
CMD ["python3", "scripts/train.py"]