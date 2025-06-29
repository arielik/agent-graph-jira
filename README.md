# Agent Graph JIRA

An intelligent agentic AI solution for automated JIRA story generation using LangGraph, designed to streamline the process of creating detailed, actionable user stories from simple YAML configurations.

## 🚀 Overview

This project leverages cutting-edge AI technologies to transform basic story outlines into comprehensive JIRA issues. The system reads YAML configuration files, uses Large Language Models (LLMs) to expand and refine story details, and automatically creates well-structured JIRA stories with proper acceptance criteria, technical considerations, and detailed descriptions.

## 🏗️ Architecture

The project follows a modular, professional architecture designed for scalability and maintainability:

```
agent-graph-jira/
├── data/                    # Data storage and persistence
├── docs/                    # Documentation of the project 
├── notebooks/               # Jupyter notebooks for experimentation
├── src/                     # Main source code
│   ├── core/                # Core business logic
│   │   ├── agent/           # LangGraph agent implementation
│   │   ├── prompts/         # AI prompt templates
│   │   └── tools/           # JIRA integration tools
│   ├── utils/               # Utility functions
│   └── infrastructure/      # External service integrations
│       ├── vector_database/ # RAG and vector storage
│       └── llm_clients/     # LLM provider clients
├── tools/                   # Development and automation tools
├── tests/                   # Comprehensive test suite
└── examples/                # Example configurations
```

## ✨ Features

- **🤖 Intelligent Story Expansion**: Uses advanced LLMs to transform basic story outlines into detailed, actionable user stories
- **🔗 Seamless JIRA Integration**: Direct integration with JIRA Cloud instances for automated issue creation
- **📊 LangGraph Workflow**: Sophisticated agent workflow using LangGraph for reliable, stateful processing
- **🎯 Configurable Templates**: Customizable prompt templates for different story types and domains
- **🔍 RAG Support**: Vector database integration for context-aware story generation
- **🛡️ Robust Error Handling**: Comprehensive error handling and retry mechanisms
- **🧪 Dry Run Mode**: Test configurations without creating actual JIRA issues
- **📝 Rich Logging**: Detailed logging with beautiful console output using Rich and Loguru

## 🛠️ Technology Stack

- **Framework**: Python 3.9+
- **AI/ML**: LangChain, LangGraph, OpenAI/Anthropic APIs
- **JIRA Integration**: python-jira library
- **Vector Database**: ChromaDB, FAISS
- **Configuration**: Pydantic, PyYAML
- **CLI**: Typer
- **Logging**: Loguru
- **Testing**: pytest, pytest-asyncio
- **Code Quality**: Black, isort, flake8, mypy

## 🚦 Getting Started

### Prerequisites

- Python 3.9 or higher
- JIRA Cloud instance with API access
- OpenAI or Anthropic API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd agent-graph-jira
   ```

2. **Set up the development environment**:
   ```bash
   make dev-setup
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual configuration values
   ```

4. **Install dependencies**:
   ```bash
   make install-dev
   ```

### Configuration

Edit the `.env` file with your credentials:

```env
# JIRA Configuration
JIRA_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@example.com
JIRA_API_TOKEN=your-jira-api-token
JIRA_PROJECT_KEY=YOUR_PROJECT

# LLM Configuration
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key

# Additional settings...
```

## 📖 Usage

### Basic Usage

1. **Create a story configuration file** (see `examples/example-stories.yaml`):

```yaml
global:
  project: "PROJ"
  labels:
    - "ai-generated"
  components:
    - "Backend"

stories:
  - title: "User Authentication System"
    description: "Implement secure user authentication"
    priority: "High"
    labels:
      - "security"
    components:
      - "Authentication"
```

2. **Run the agent**:
   ```bash
   # Dry run (recommended first)
   make run-example --dry-run
   
   # Actual execution
   agent-jira run --config examples/example-stories.yaml
   ```

3. **Validate configuration**:
   ```bash
   agent-jira validate --config examples/example-stories.yaml
   ```

### Advanced Usage

- **Custom configuration**:
  ```bash
  agent-jira run --config path/to/your/config.yaml --verbose
  ```

- **Development mode**:
  ```bash
  python -m src.main --config examples/example-stories.yaml --dry-run
  ```

## 🔧 Development

### Project Structure Explained

- **`src/core/agent/`**: Contains the main LangGraph agent implementation that orchestrates the story processing workflow
- **`src/core/prompts/`**: Houses AI prompt templates optimized for different story expansion scenarios
- **`src/core/tools/`**: JIRA integration tools and other utilities used by the agent
- **`src/infrastructure/`**: External service integrations (LLM clients, vector databases)
- **`src/utils/`**: Common utilities for configuration, logging, and helper functions
- **`notebooks/`**: Jupyter notebooks for experimentation, prototyping, and analysis
- **`data/`**: Persistent storage for vector databases, logs, and other data

### Development Workflow

1. **Code formatting**:
   ```bash
   make format
   ```

2. **Linting**:
   ```bash
   make lint
   ```

3. **Testing**:
   ```bash
   make test
   ```

4. **Full development cycle**:
   ```bash
   make format lint test
   ```

## 🧪 Testing

The project includes comprehensive tests covering:

- Configuration loading and validation
- JIRA API integration
- LLM client functionality
- Agent workflow execution
- Error handling scenarios

Run tests with:
```bash
pytest tests/ -v --cov=src
```

## 📊 LangGraph Workflow

The agent uses a sophisticated LangGraph workflow:

1. **Load Stories**: Parse YAML configuration and load story definitions
2. **Process Story**: Select and prepare individual stories for processing
3. **Expand Story**: Use LLM to generate detailed story content with acceptance criteria
4. **Create JIRA Issue**: Transform expanded content into JIRA issue and create it
5. **Error Handling**: Robust error handling with retry mechanisms

## 🎯 YAML Configuration Schema

```yaml
global:                    # Global configuration (optional)
  project: "PROJECT_KEY"   # Default JIRA project
  labels: []              # Default labels
  components: []          # Default components
  epic: "EPIC-123"        # Default epic link

stories:                  # Array of stories to process
  - title: "Story Title"  # Required: Story title
    description: "..."    # Required: Story description
    priority: "High"      # Optional: Priority level
    labels: []           # Optional: Story-specific labels
    components: []       # Optional: Story-specific components
    issue_type: "Story"  # Optional: JIRA issue type
    project: "PROJ"      # Optional: Override global project
```

## 🔍 Monitoring and Logging

The system provides comprehensive logging and monitoring:

- **Rich console output** with colored, formatted messages
- **Structured logging** with contextual information
- **Performance metrics** and timing information
- **Error tracking** with detailed stack traces
- **Dry-run reporting** for testing configurations

## 🚀 Deployment

For production deployment:

1. **Build Docker image**:
   ```bash
   make docker-build
   ```

2. **Run containerized**:
   ```bash
   make docker-run
   ```

3. **Environment-specific configuration**:
   - Use separate `.env` files for different environments
   - Configure appropriate logging levels
   - Set up monitoring and alerting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes following the code style guidelines
4. Run tests: `make test`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Style Guidelines

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Write comprehensive docstrings
- Add tests for new functionality
- Keep functions focused and small

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
- Uses [LangChain](https://github.com/langchain-ai/langchain) for LLM integration
- JIRA integration powered by [python-jira](https://github.com/pycontribs/jira)
- CLI interface built with [Typer](https://github.com/tiangolo/typer)

## 📞 Support

For support, questions, or contributions:

- Create an issue in the GitHub repository
- Check the documentation in the `docs/` directory
- Review example configurations in `examples/`

---

**Built with ❤️ for streamlined JIRA story creation using AI**
Agentic aproach to aut populate stories based on simple engineer feedback, useful for personal/small teams pipelines
