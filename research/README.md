# Research Crew

Welcome to the Research Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:

```bash
poetry lock
```

```bash
poetry install
```

## Configuration

To switch between `ChatOpenAI` and `ChatGroq` for agent initialization, set the `AGENT_MODEL` environment variable to either `ChatOpenAI` or `ChatGroq`. This allows for easy switching between the two models without altering the codebase.

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
poetry run research
```

## Notes

- When max_iteration is set to 2, gpt4-o returns a fail with 'Agent stopped due to iteration limit or time limit.'
