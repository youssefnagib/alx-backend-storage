# 0x02-redis_basic

This repository contains basic concepts and implementations using Redis, a fast, open-source, in-memory key-value data store. The project focuses on understanding how to work with Redis in Python, leveraging its speed and data structure support.

## Learning Objectives

By the end of this project, you should be able to:

- Understand what Redis is and how it works.
- Explain why Redis is used and its advantages.
- Set up and interact with a Redis database.
- Use Redis commands to perform basic operations like setting, getting, and deleting data.
- Implement caching using Redis in Python.
- Explain persistence options in Redis.

## Technologies

- Python 3.8+
- Redis 4.0+
- `redis-py` Python package
- Redis CLI

## Project Structure

The repository includes the following files and directories:

- `basic_redis.py`: Python file containing the basic Redis client interactions.
- `cache.py`: A caching system implemented using Redis.
- `main.py`: Sample script for testing Redis functionality.
- `README.md`: This file.

## Setup

1. Install Redis on your system:
   - For Linux or macOS, you can use package managers like `apt`, `brew`, or build from source.
   - For Windows, use Redis on WSL (Windows Subsystem for Linux) or a Docker container.

2. Install Python dependencies:
   ```bash
   pip install redis
