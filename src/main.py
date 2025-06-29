"""Main entry point for the Agent Graph JIRA application."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer
from loguru import logger
from rich.console import Console

from src.core.agent.jira_agent import JiraAgent
from src.utils.config import load_config
from src.utils.logging import setup_logging

app = typer.Typer(
    name="agent-jira",
    help="Agentic AI solution for automated JIRA story generation using LangGraph",
)

console = Console()


@app.command()
def run(
    config_file: Path = typer.Option(
        "examples/example-stories.yaml",
        "--config",
        "-c",
        help="Path to the YAML configuration file",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Run without actually creating JIRA stories",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose logging",
    ),
) -> None:
    """Run the JIRA agent to process stories from a YAML configuration file."""
    
    # Setup logging
    log_level = "DEBUG" if verbose else "INFO"
    setup_logging(log_level)
    
    try:
        # Load configuration
        config = load_config(config_file)
        logger.info(f"Loaded configuration from {config_file}")
        
        # Initialize and run the agent
        agent = JiraAgent(config, dry_run=dry_run)
        
        console.print(f"[bold green]Starting JIRA Agent[/bold green]")
        console.print(f"Config file: {config_file}")
        console.print(f"Dry run: {dry_run}")
        
        # Run the agent
        asyncio.run(agent.process_stories())
        
        console.print("[bold green]✅ Agent execution completed successfully![/bold green]")
        
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def validate(
    config_file: Path = typer.Option(
        "examples/example-stories.yaml",
        "--config",
        "-c",
        help="Path to the YAML configuration file to validate",
    ),
) -> None:
    """Validate a YAML configuration file."""
    
    try:
        config = load_config(config_file)
        console.print(f"[bold green]✅ Configuration file {config_file} is valid![/bold green]")
        
        # Print summary
        stories_count = len(config.get("stories", []))
        console.print(f"Found {stories_count} stories to process")
        
    except Exception as e:
        console.print(f"[bold red]❌ Configuration validation failed: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def version() -> None:
    """Show the application version."""
    from src import __version__
    console.print(f"Agent Graph JIRA v{__version__}")


def main() -> None:
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
