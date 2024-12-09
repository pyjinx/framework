from typing import Any, Callable, Dict, List, Optional, Protocol, Union
from Illuminate.Foundation.Console.Command import Command
from Illuminate.Foundation.Console.Input.ArgvInput import ArgvInput
from Illuminate.Foundation.Console.Output.ConsoleOutput import ConsoleOutput
from Illuminate.Contracts.Foundation.Application import (
    Application as ApplicationContract,
)


class Application(Protocol):
    def __init__(self, app: ApplicationContract, events: Any, version: str) -> None:
        """
        Initialize the console application with the given dependencies.
        """
        pass

    @classmethod
    def starting(cls, callbacks: Callable[..., Any]) -> None:
        """
        Register a callback to be invoked when the application is starting.
        """
        pass

    def bootstrap(self) -> None:
        """
        Bootstrap the application with registered bootstrappers.
        """
        pass

    def run(self, input: ArgvInput, output: ConsoleOutput) -> None:
        """
        Run the application with the provided input and output.
        """
        pass

    def terminate(self) -> None:
        """
        Terminate the application gracefully.
        """
        pass

    def call_silent(
        self, command: str, arguments: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Call a command silently.
        """
        pass

    def call(
        self,
        command: str,
        arguments: Optional[Dict[str, Any]] = None,
        silent: bool = False,
    ) -> Any:
        """
        Call a command with the provided arguments.
        """
        pass

    def resolve_commands(
        self, commands: Union[List[Command], Command]
    ) -> "ApplicationContract":
        """
        Resolve and register one or more commands to the application.
        """
        pass

    def resolve(self, command: Union[Command, type]) -> Command:
        """
        Resolve a command and add it to the application.
        """
        pass

    def add(self, command: Command) -> Command:
        """
        Add a command instance to the application.
        """
        pass

    def set_container_command_loader(self) -> "ApplicationContract":
        """
        Set the container-based command loader for the application.
        """
        pass
