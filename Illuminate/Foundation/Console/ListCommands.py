from colorama import Fore, Style

from Illuminate.Collections.helpers import collect
from Illuminate.Contracts.Foundation.Console.Kernel import (
    Kernel as ConsoleKernelContract,
)
from Illuminate.Foundation.Console.Command import Command


class ListCommands(Command):
    name = "list"
    description = "List all commands"

    def handle(self):
        kernel = self.application.make(ConsoleKernelContract)

        commander = kernel.get_commander()

        padding = 4

        self.info(f"PyJinx Framework {self.commander.version}")

        self.new_line()

        self.info("Usage:")

        self.line(" " * padding + "Commands [options] [arguments]")

        self.new_line()

        self.info("Options:")

        max_length = self._get_max_length(self.options, commander.command_map.items())

        description_start = padding + max_length + padding

        for option in self.options:
            description_text = Fore.WHITE + option["description"]

            self.success(
                " " * padding
                + option["name"].ljust(description_start + padding)
                + description_text
            )

        self.new_line()

        self.info("Available Commands:")

        commands = collect(commander.command_map).group_by(lambda item: item.segment)

        for group_key, group_commands in commands:
            if group_key:
                print(f"{Fore.YELLOW}{group_key}{Style.RESET_ALL}")

            for key, item in group_commands:
                if not item.hidden:
                    command_text = (
                        " " * padding
                        + item.name.ljust(description_start + padding)
                    )
                    print(
                        f"{Fore.GREEN}{command_text}{Style.RESET_ALL}"
                        f"{Fore.WHITE}{item.description}{Style.RESET_ALL}"
                    )

        self.new_line()

        exit()

    def _get_max_length(self, options: list, commands: list):
        max_option_length = max(len(option["name"]) for option in options)

        max_command_length = max(
            len(item.name) for key, item in commands if not item.hidden
        )

        return max([max_option_length, max_command_length])
