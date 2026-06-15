from enum import Enum, IntEnum


class ForegroundColor(IntEnum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

class BackgroundColor(IntEnum):
    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47


class Fonts(IntEnum):
    BOLD = 1
    FAINT = 2
    ITALIC = 3


class Decorators(IntEnum):
    UNDERLINE = 4
    DOUBLE_UNDERLINE = 21
    STRIKE = 9
    OVERLINE = 53


class Effects(IntEnum):
    BLINK = 5
    REVERSE = 7
    HIDDEN = 8


class Reset(IntEnum):
    RESET = 0


class CursorMovement(Enum):
    UP = "A"
    DOWN = "B"
    RIGHT = "C"
    LEFT = "D"


class CursorVisibility(Enum):
    HIDE = "?25l"
    SHOW = "?25h"


class LineNavigation(Enum):
    NEXT = "E"
    PREV = "F"


class Erasing(Enum):
    SCREEN = "2J"
    SCROLL = "3J"
    LINE = "K"
    TO_START = "1K"


class Teleportation(Enum):
    HOME = "H"
    SAVE = "s"
    RESTORE = "u"


class Ansi:
    @staticmethod
    def ansi(*commands) -> str:
        flattened_commands = []
        for command in commands:
            if isinstance(command, (list, tuple)):
                flattened_commands.extend(command)
            else:
                flattened_commands.append(command)

        flattened_commands = [
            command for command in flattened_commands if command is not None
        ]

        if not flattened_commands:
            return ""

        styling_codes = [
            str(command) for command in flattened_commands if isinstance(command, int)
        ]
        action_codes = [
            str(command) for command in flattened_commands if isinstance(command, str)
        ]

        output_sequences = []
        if styling_codes:
            output_sequences.append(f"\033[{";".join(styling_codes)}m")

        for code in action_codes:
            output_sequences.append(f"\033[{code}")

        return "".join(output_sequences)

    class _ResetContext:
        def __enter__(self):
            return Ansi.ansi

        def __exit__(self, *exceptions):
            print(Ansi.ansi(Reset.RESET), end="")

    reset = _ResetContext()
    clear = "\033[2J\033[H"
