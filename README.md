# Language POC

This repository contains a proof of concept for language processing using LangGraph and LLM integration.

## Requirements

- Python 3.11
- UV package manager (recommended) or pip

## Installation

### 1. Install UV (if not already installed)

```bash
# Install UV using the official installer
curl -sSf https://install.ultraviolet.dev | sh

# Or with pip
pip install uv
```

### 2. Clone the repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 3. Create and activate a virtual environment

```bash
# Using UV
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On Linux/macOS
# OR
.venv\Scripts\activate     # On Windows
```

### 4. Install dependencies

```bash
# Using UV
uv pip install -e .

# Or using pip
pip install -e .
```

## Usage

Make sure your virtual environment is activated, then run:

```bash
python src/lang_poc/main.py
```

You may need to set your API keys as environment variables:
- `ANTHROPIC_API_KEY` for Anthropic Claude models
- `OPENAI_API_KEY` for OpenAI models
