# Vision-Language-Action (VLA) Integration for ROS 2

This project implements a Vision-Language-Action (VLA) integration system that enables students to issue voice and text commands processed by LLMs and translated into ROS 2 actions for simulated humanoid robots.

## Prerequisites

- Python 3.8 or higher
- ROS 2 Humble Hawksbill
- OpenAI API key
- Docker (optional, for containerized deployment)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Set up Python virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Copy the example environment file and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_openai_api_key_here
```

### 5. Install additional tools (optional)

For development and testing:

```bash
pip install pytest pytest-asyncio black flake8 mypy
```

## Running the Service

### 1. Start the VLA service

```bash
cd src/vla
python -m api.main
```

Or using uvicorn:

```bash
uvicorn src.vla.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Test the service

Once running, the service will be available at `http://localhost:8000`.

## Project Structure

```
src/vla/
├── api/                 # FastAPI endpoints
├── models/              # Data models
├── services/            # Business logic
├── utils/               # Utility functions
├── tests/               # Test files
├── config.py            # Configuration settings
└── __init__.py          # Package initialization
```

## Development

### Code Formatting

This project uses Black for code formatting. Format your code before committing:

```bash
black src/
```

### Linting

Use flake8 for linting:

```bash
flake8 src/
```

### Testing

Run tests with pytest:

```bash
pytest tests/
```

## Configuration

The service can be configured through environment variables. See `.env.example` for all available options.

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**: Make sure your `OPENAI_API_KEY` is set correctly in `.env`
2. **ROS 2 Connection Issues**: Ensure ROS 2 environment is sourced properly
3. **Port Already in Use**: Change `VLA_SERVICE_PORT` in your `.env` file

## License

MIT License - See LICENSE file for details.