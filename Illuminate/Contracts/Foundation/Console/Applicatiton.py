from collections.abc import Callable
from typing import Any, Protocol

from Illuminate.Contracts.Foundation.Application import (
    Application as ApplicationContract,
)
from Illuminate.Foundation.Console.Command import Command
from Illuminate.Foundation.Console.Input.ArgvInput import ArgvInput
from Illuminate.Foundation.Console.Output.ConsoleOutput import ConsoleOutput


class Application(Protocol):
    def __init__(self, app: ApplicationContract, events: Any, version: str) -> None:
        """
        Initialize the console application with the given dependencies.
        """

    @classmethod
    def starting(cls, callbacks: Callable[..., Any]) -> None:
        """
        Register a callback to be invoked when the application is starting.
        """

    def bootstrap(self) -> None:
        """
        Bootstrap the application with registered bootstrappers.
        """

    def run(self, input: ArgvInput, output: ConsoleOutput) -> None:
        """
        Run the application with the provided input and output.
        """

    def terminate(self) -> None:
        """
        Terminate the application gracefully.
        """

    def call_silent(
        self, command: str, arguments: dict[str, Any] | None = None
    ) -> Any:
        """
        Call a command silently.
        """

    def call(
        self,
        command: str,
        arguments: dict[str, Any] | None = None,
        silent: bool = False,
    ) -> Any:
        """
        Call a command with the provided arguments.
        """

    def resolve_commands(
        self, commands: list[Command] | Command
    ) -> "ApplicationContract":
        """
        Resolve and register one or more commands to the application.
        """

    def resolve(self, command: Command | type) -> Command:
        """
        Resolve a command and add it to the application.
        """

    def add(self, command: Command) -> Command:
        """
        Add a command instance to the application.
        """

    def set_container_command_loader(self) -> "ApplicationContract":
        """
        Set the container-based command loader for the application.
        """
