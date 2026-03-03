# 1. Use NVIDIA CUDA base
FROM nvidia/cuda:12.1.1-devel-ubuntu22.04

# 2. Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# 3. Install build dependencies
RUN apt-get update && apt-get install -y \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libsqlite3-dev \
    libreadline-dev \
    libffi-dev \
    curl \
    libbz2-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# 4. Download, Compile, and Install Python 3.12.10
# We use --prefix=/usr to place it in /usr/bin/ instead of /usr/local/bin/
# This makes it easier for system tools to find it.
RUN wget https://www.python.org/ftp/python/3.12.10/Python-3.12.10.tgz \
    && tar -xf Python-3.12.10.tgz \
    && cd Python-3.12.10 \
    && ./configure --enable-optimizations --with-ensurepip=install --prefix=/usr \
    && make -j$(nproc) \
    && make install \
    && cd .. && rm -rf Python-3.12.10*

# 5. Set Python 3.12 as the default python3 and python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 \
    && update-alternatives --set python3 /usr/bin/python3.12 \
    && ln -sf /usr/bin/python3.12 /usr/bin/python

# 6. Install Poetry (using the now-linked python3)
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# 7. Copy ONLY dependency files for better caching
COPY pyproject.toml poetry.lock* ./

# 8. Install dependencies
# We turn off virtualenvs because Docker provides the isolation we need
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# 9. Copy the rest of the project
COPY . .

# 10. Default command
CMD ["python3", "scripts/train.py"]