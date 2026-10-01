# Ansirithm

### A Python ANSI utility with slightly fewer terminal-related inconveniences.

Welcome to **Ansirithm**, a lightweight Python utility for generating ANSI escape sequences for terminal styling, cursor control, screen manipulation, and text decoration.

Ansirithm provides a small collection of enums and helper functionality for constructing ANSI escape sequences without requiring raw escape-code strings throughout your application.

Ansirithm provides several conveniences:

- **Foreground colors** through `ForegroundColor`.
- **Background colors** through `BackgroundColor`.
- **Font styles** such as bold, faint, and italic.
- **Text decorators** including underline, strike-through, and overline.
- **Terminal effects** such as blinking, reverse video, and hidden text.
- **Cursor movement** through directional ANSI sequences.
- **Cursor visibility control** for hiding and showing the terminal cursor.
- **Line navigation** for moving between terminal lines.
- **Screen and line erasing** through standard ANSI erase sequences.
- **Cursor teleportation** for home, save, and restore operations.
- **Automatic ANSI sequence construction** through `Ansi.ansi()`.
- **Context-managed reset behavior** through `Ansi.reset`.

Ansirithm intentionally keeps ANSI terminal control explicit while providing readable names for otherwise mysterious numerical escape codes.

It is designed for programmers who would rather write:

```python
Ansi.ansi(ForegroundColor.RED)
```

than remember that red is apparently `31`.

Because naturally terminals require a secret numerical language to change the color of text.

---

## 1. Installation

Ansirithm uses Python's standard library and does not require external dependencies.

Import the required classes from the Ansirithm module.

```python
from ansirithm import (
    Ansi,
    ForegroundColor,
    BackgroundColor,
    Fonts,
    Decorators,
    Effects,
    Reset,
    CursorMovement,
    CursorVisibility,
    LineNavigation,
    Erasing,
    Teleportation,
)
```

Replace `ansirithm` with the module path used by your installation.

Ansirithm generates standard ANSI escape sequences that can be written directly to terminal output.

---

## 2. ANSI Sequence Generation

The primary interface for generating escape sequences is:

```python
Ansi.ansi(*codes)
```

The method accepts any number of ANSI style codes or action strings.

Example:

```python
print(
    Ansi.ansi(ForegroundColor.RED)
    + "Hello"
    + Ansi.ansi(Reset.RESET)
)
```

This produces red text followed by a terminal style reset.

Multiple codes can be combined in a single call.

```python
Ansi.ansi(
    ForegroundColor.RED,
    Fonts.BOLD
)
```

The resulting sequence applies both styles.

---

## 3. ANSI Code Categories

Ansirithm separates ANSI codes into several categories according to their purpose.

### 3.1 Styling Codes

Styling codes are integer-based ANSI SGR values.

They include:

- Foreground colors.
- Background colors.
- Fonts.
- Decorations.
- Effects.
- Reset operations.

These codes are combined into a single SGR escape sequence.

### 3.2 Action Codes

Action codes are string-based ANSI escape sequences used for terminal operations such as:

- Cursor movement.
- Cursor visibility.
- Line navigation.
- Screen erasing.
- Cursor positioning.

These sequences are emitted individually.

---

## 4. Foreground Colors

The `ForegroundColor` enum provides standard ANSI foreground colors.

| Color | ANSI Code |
|---|---:|
| `BLACK` | `30` |
| `RED` | `31` |
| `GREEN` | `32` |
| `YELLOW` | `33` |
| `BLUE` | `34` |
| `MAGENTA` | `35` |
| `CYAN` | `36` |
| `WHITE` | `37` |

### Example

```python
print(
    Ansi.ansi(ForegroundColor.RED)
    + "Red text"
    + Ansi.ansi(Reset.RESET)
)
```

Multiple styles can be combined:

```python
print(
    Ansi.ansi(
        ForegroundColor.GREEN,
        Fonts.BOLD
    )
    + "Bold green text"
    + Ansi.ansi(Reset.RESET)
)
```

The color remains active until another ANSI style sequence changes it or the terminal is reset.

Terminals, like humans, occasionally need to be explicitly told when something is over.

---

## 5. Background Colors

The `BackgroundColor` enum provides standard ANSI background colors.

| Color | ANSI Code |
|---|---:|
| `BLACK` | `40` |
| `RED` | `41` |
| `GREEN` | `42` |
| `YELLOW` | `43` |
| `BLUE` | `44` |
| `MAGENTA` | `45` |
| `CYAN` | `46` |
| `WHITE` | `47` |

### Example

```python
print(
    Ansi.ansi(BackgroundColor.BLUE)
    + "Blue background"
    + Ansi.ansi(Reset.RESET)
)
```

Foreground and background colors can be combined.

```python
print(
    Ansi.ansi(
        ForegroundColor.WHITE,
        BackgroundColor.BLUE
    )
    + "White on blue"
    + Ansi.ansi(Reset.RESET)
)
```

---

## 6. Fonts

The `Fonts` enum provides common ANSI text styles.

| Style | ANSI Code |
|---|---:|
| `BOLD` | `1` |
| `FAINT` | `2` |
| `ITALIC` | `3` |

### Example

```python
print(
    Ansi.ansi(Fonts.BOLD)
    + "Bold text"
    + Ansi.ansi(Reset.RESET)
)
```

Multiple font-related styles may be supplied together.

```python
Ansi.ansi(
    Fonts.BOLD,
    Fonts.ITALIC
)
```

Terminal support for individual styles may vary depending on the terminal emulator.

ANSI is a standard.

Terminal behavior is apparently more of a suggestion.

---

## 7. Text Decorators

The `Decorators` enum provides ANSI text decoration codes.

| Decorator | ANSI Code |
|---|---:|
| `UNDERLINE` | `4` |
| `DOUBLE_UNDERLINE` | `21` |
| `STRIKE` | `9` |
| `OVERLINE` | `53` |

### Example

```python
print(
    Ansi.ansi(Decorators.UNDERLINE)
    + "Underlined text"
    + Ansi.ansi(Reset.RESET)
)
```

Decorators can be combined with colors and fonts.

```python
print(
    Ansi.ansi(
        ForegroundColor.CYAN,
        Fonts.BOLD,
        Decorators.UNDERLINE
    )
    + "Styled text"
    + Ansi.ansi(Reset.RESET)
)
```

---

## 8. Terminal Effects

The `Effects` enum provides ANSI terminal effects.

| Effect | ANSI Code |
|---|---:|
| `BLINK` | `5` |
| `REVERSE` | `7` |
| `HIDDEN` | `8` |

### Example

```python
print(
    Ansi.ansi(Effects.REVERSE)
    + "Reverse video"
    + Ansi.ansi(Reset.RESET)
)
```

Blinking behavior depends on terminal support.

The `HIDDEN` effect is commonly used for concealing terminal text, although terminal behavior can vary.

---

## 9. Reset

The `Reset` enum currently provides a single reset operation.

| Operation | ANSI Code |
|---|---:|
| `RESET` | `0` |

Use it to return terminal styling to its default state.

```python
print(
    Ansi.ansi(ForegroundColor.RED)
    + "Red"
    + Ansi.ansi(Reset.RESET)
    + " Normal"
)
```

The reset sequence prevents styles from unintentionally affecting subsequent output.

This is particularly important when writing reusable terminal applications.

Otherwise your entire terminal may suddenly become red because one line of code got ambitious.

---

## 10. Cursor Movement

The `CursorMovement` enum provides directional cursor movement sequences.

| Direction | ANSI Command |
|---|---|
| `UP` | `A` |
| `DOWN` | `B` |
| `RIGHT` | `C` |
| `LEFT` | `D` |

These commands are represented as ANSI CSI sequences.

### Example

```python
print(
    Ansi.ansi(
        CursorMovement.UP.value
    )
)
```

The cursor movement command itself does not specify a distance.

ANSI interprets an omitted movement parameter according to its standard default behavior.

---

## 11. Cursor Visibility

The `CursorVisibility` enum controls whether the terminal cursor is visible.

| Operation | ANSI Sequence |
|---|---|
| `HIDE` | `?25l` |
| `SHOW` | `?25h` |

### Hide the Cursor

```python
print(
    Ansi.ansi(
        CursorVisibility.HIDE.value
    ),
    end=""
)
```

### Show the Cursor

```python
print(
    Ansi.ansi(
        CursorVisibility.SHOW.value
    ),
    end=""
)
```

Cursor visibility control is useful for terminal interfaces, animations, progress displays, and other applications where a blinking cursor wandering around the screen would be less than helpful.

---

## 12. Line Navigation

The `LineNavigation` enum provides ANSI sequences for moving between terminal lines.

| Operation | ANSI Command |
|---|---|
| `NEXT` | `E` |
| `PREV` | `F` |

### Example

```python
print(
    Ansi.ansi(
        LineNavigation.NEXT.value
    )
)
```

The commands are emitted as ANSI CSI sequences by `Ansi.ansi()`.

---

## 13. Erasing

The `Erasing` enum provides ANSI commands for clearing terminal content.

| Operation | ANSI Command |
|---|---|
| `SCREEN` | `2J` |
| `SCROLL` | `3J` |
| `LINE` | `K` |
| `TO_START` | `1K` |

### Clear the Screen

```python
print(
    Ansi.ansi(
        Erasing.SCREEN.value
    ),
    end=""
)
```

### Clear the Current Line

```python
print(
    Ansi.ansi(
        Erasing.LINE.value
    ),
    end=""
)
```

### Clear to the Start of the Line

```python
print(
    Ansi.ansi(
        Erasing.TO_START.value
    ),
    end=""
)
```

These operations allow terminal applications to manipulate visible output without relying exclusively on ordinary newline-based printing.

---

## 14. Teleportation

The `Teleportation` enum provides cursor-positioning and cursor-state commands.

| Operation | ANSI Command |
|---|---|
| `HOME` | `H` |
| `SAVE` | `s` |
| `RESTORE` | `u` |

### Home

The `HOME` sequence moves the cursor to the terminal's home position.

```python
print(
    Ansi.ansi(
        Teleportation.HOME.value
    ),
    end=""
)
```

### Save Position

```python
print(
    Ansi.ansi(
        Teleportation.SAVE.value
    ),
    end=""
)
```

### Restore Position

```python
print(
    Ansi.ansi(
        Teleportation.RESTORE.value
    ),
    end=""
)
```

Saving and restoring cursor position can be useful when temporarily writing terminal output and then returning to the previous cursor location.

A surprisingly useful ability for something that sounds like a science-fiction feature.

---

## 15. Combining Styles

Multiple integer-based ANSI styles can be passed to `Ansi.ansi()` at once.

```python
style = Ansi.ansi(
    ForegroundColor.YELLOW,
    BackgroundColor.BLUE,
    Fonts.BOLD,
    Decorators.UNDERLINE
)

print(
    style
    + "Important message"
    + Ansi.ansi(Reset.RESET)
)
```

All integer codes are combined into a single ANSI SGR sequence.

Conceptually, the generated sequence is equivalent to:

```text
ESC[33;44;1;4m
```

followed by the provided text and then a reset sequence.

This allows complex terminal styling without manually constructing ANSI escape strings.

---

## 16. Nested Code Collections

`Ansi.ansi()` also accepts lists and tuples.

For example:

```python
styles = [
    ForegroundColor.CYAN,
    Fonts.BOLD,
    Decorators.UNDERLINE
]

print(
    Ansi.ansi(styles)
    + "Styled text"
    + Ansi.ansi(Reset.RESET)
)
```

Nested collections can also be supplied alongside individual codes.

```python
styles = [
    ForegroundColor.GREEN,
    Fonts.BOLD
]

Ansi.ansi(
    styles,
    Decorators.UNDERLINE
)
```

Lists and tuples are flattened by one level before processing.

This makes it possible to construct reusable style collections.

---

## 17. Ignoring `None`

`Ansi.ansi()` ignores `None` values.

This allows conditional styling to be constructed conveniently.

```python
color = ForegroundColor.RED
optional_style = None

sequence = Ansi.ansi(
    color,
    optional_style,
    Fonts.BOLD
)
```

The `None` value is simply omitted.

This is useful when building terminal styles dynamically.

---

## 18. Empty ANSI Sequences

If no usable codes are supplied, `Ansi.ansi()` returns an empty string.

```python
Ansi.ansi()
```

Result:

```text
""
```

Likewise:

```python
Ansi.ansi(None, [], ())
```

produces an empty string.

This allows ANSI sequence generation to safely participate in conditional formatting without requiring special handling for every empty case.

---

## 19. The Reset Context Manager

Ansirithm provides a small context manager through:

```python
Ansi.reset
```

The object can be used with Python's `with` statement.

```python
with Ansi.reset():
    print("Styled output")
```

The context manager's `__enter__()` method returns `Ansi.ansi`.

When the context exits, the reset sequence is printed automatically.

The intended purpose is to make temporary terminal styling easier to manage.

### Example

```python
with Ansi.reset() as ansi:
    print(
        ansi(
            ForegroundColor.RED,
            Fonts.BOLD
        )
        + "Temporary style"
    )
```

After the block completes, Ansirithm emits:

```text
ESC[0m
```

This ensures the terminal returns to its default styling state.

No cleanup code required.

Because forgetting to reset terminal colors is how innocent shell sessions become crime scenes.

---

## 20. Clearing the Terminal

Ansirithm provides a predefined `clear` sequence.

```python
Ansi.clear
```

The value is:

```text
ESC[2J ESC[H
```

In Python:

```python
print(Ansi.clear, end="")
```

This performs two operations:

1. Clears the terminal screen.
2. Moves the cursor to the home position.

The sequence can therefore be used as a convenient terminal-clearing operation.

---

## 21. Complete Example: Styled Terminal Output

The following example demonstrates colors, fonts, decorations, resetting, and cursor control.

```python
from ansirithm import (
    Ansi,
    ForegroundColor,
    BackgroundColor,
    Fonts,
    Decorators,
    Reset,
)

title = Ansi.ansi(
    ForegroundColor.CYAN,
    Fonts.BOLD,
    Decorators.UNDERLINE
)

warning = Ansi.ansi(
    ForegroundColor.YELLOW,
    BackgroundColor.RED,
    Fonts.BOLD
)

print(
    title
    + "Ansirithm"
    + Ansi.ansi(Reset.RESET)
)

print(
    warning
    + "Warning"
    + Ansi.ansi(Reset.RESET)
)

print("Normal terminal output.")
```

The program demonstrates the basic Ansirithm workflow:

1. Construct an ANSI style.
2. Print styled text.
3. Reset the terminal style.
4. Continue with normal output.

---

## 22. Complete Example: Cursor Control

The following example demonstrates cursor visibility, screen clearing, and cursor positioning.

```python
from ansirithm import (
    Ansi,
    CursorVisibility,
    Erasing,
    Teleportation,
)

# Hide the cursor

print(
    Ansi.ansi(CursorVisibility.HIDE.value),
    end=""
)

# Clear the screen

print(
    Ansi.ansi(Erasing.SCREEN.value),
    end=""
)

# Move to the home position

print(
    Ansi.ansi(Teleportation.HOME.value),
    end=""
)

print("Ansirithm terminal demo")

# Restore cursor visibility

print(
    Ansi.ansi(CursorVisibility.SHOW.value),
    end=""
)
```

This demonstrates how Ansirithm can be used for simple terminal interfaces and screen-based applications.

---

## 23. Complete Example: Dynamic Styling

Because `Ansi.ansi()` accepts collections and optional values, styles can be assembled dynamically.

```python
from ansirithm import (
    Ansi,
    ForegroundColor,
    Fonts,
    Decorators,
)

styles = [
    ForegroundColor.MAGENTA,
    Fonts.BOLD,
]

underline = Decorators.UNDERLINE

sequence = Ansi.ansi(
    styles,
    underline
)

print(
    sequence
    + "Dynamic styling"
    + Ansi.ansi(0)
)
```

This approach makes it possible to construct reusable terminal themes.

For example:

```python
SUCCESS = Ansi.ansi(
    ForegroundColor.GREEN,
    Fonts.BOLD
)

ERROR = Ansi.ansi(
    ForegroundColor.RED,
    Fonts.BOLD
)

INFO = Ansi.ansi(
    ForegroundColor.CYAN
)
```

These styles can then be reused throughout an application.

---

## 24. API Summary

### Foreground Colors

```python
ForegroundColor.BLACK
ForegroundColor.RED
ForegroundColor.GREEN
ForegroundColor.YELLOW
ForegroundColor.BLUE
ForegroundColor.MAGENTA
ForegroundColor.CYAN
ForegroundColor.WHITE
```

### Background Colors

```python
BackgroundColor.BLACK
BackgroundColor.RED
BackgroundColor.GREEN
BackgroundColor.YELLOW
BackgroundColor.BLUE
BackgroundColor.MAGENTA
BackgroundColor.CYAN
BackgroundColor.WHITE
```

### Fonts

```python
Fonts.BOLD
Fonts.FAINT
Fonts.ITALIC
```

### Decorators

```python
Decorators.UNDERLINE
Decorators.DOUBLE_UNDERLINE
Decorators.STRIKE
Decorators.OVERLINE
```

### Effects

```python
Effects.BLINK
Effects.REVERSE
Effects.HIDDEN
```

### Reset

```python
Reset.RESET
```

### Cursor Movement

```python
CursorMovement.UP
CursorMovement.DOWN
CursorMovement.RIGHT
CursorMovement.LEFT
```

### Cursor Visibility

```python
CursorVisibility.HIDE
CursorVisibility.SHOW
```

### Line Navigation

```python
LineNavigation.NEXT
LineNavigation.PREV
```

### Erasing

```python
Erasing.SCREEN
Erasing.SCROLL
Erasing.LINE
Erasing.TO_START
```

### Teleportation

```python
Teleportation.HOME
Teleportation.SAVE
Teleportation.RESTORE
```

### Main Interface

```python
Ansi.ansi(*codes)
Ansi.reset
Ansi.clear
```

---

## 25. Design Philosophy

Ansirithm is designed to provide a readable Python interface over standard ANSI terminal escape sequences.

The library deliberately represents ANSI codes using named enums rather than requiring users to memorize numerical constants and control sequences.

The architecture separates terminal functionality into logical categories:

- `ForegroundColor` handles text color.
- `BackgroundColor` handles background color.
- `Fonts` handles font-style attributes.
- `Decorators` handles text decorations.
- `Effects` handles terminal effects.
- `Reset` handles style reset operations.
- `CursorMovement` handles directional cursor movement.
- `CursorVisibility` handles cursor visibility.
- `LineNavigation` handles line-based cursor navigation.
- `Erasing` handles terminal content removal.
- `Teleportation` handles cursor positioning and position storage.

`Ansi.ansi()` then provides the common mechanism for converting these values into actual ANSI escape sequences.

Ansirithm does not attempt to replace terminal emulators or implement a terminal itself.

It simply makes the existing ANSI control system less unpleasant to use.

Which, frankly, is already a respectable contribution to civilization.

---

## 26. Limitations

Ansirithm is intentionally lightweight and currently provides only a subset of ANSI terminal functionality.

The current implementation does not provide:

- 256-color support.
- True-color RGB sequences.
- Cursor positioning with arbitrary row and column parameters.
- Terminal input handling.
- Keyboard event parsing.
- Terminal size detection.
- Platform-specific console APIs.
- Automatic terminal capability detection.
- Automatic ANSI disabling for unsupported terminals.
- Full ANSI/ECMA-48 sequence coverage.

Terminal support for individual effects may vary between terminal emulators.

The library generates ANSI sequences but does not verify whether the receiving terminal supports them.

---

## 27. Final Example

A compact Ansirithm program can therefore look like this:

```python
from ansirithm import (
    Ansi,
    ForegroundColor,
    Fonts,
    Decorators,
    Reset,
)

style = Ansi.ansi(
    ForegroundColor.CYAN,
    Fonts.BOLD,
    Decorators.UNDERLINE
)

print(
    style
    + "Hello from Ansirithm"
    + Ansi.ansi(Reset.RESET)
)
```

Output:

```text
Hello from Ansirithm
```

The terminal handles the actual styling through ANSI escape sequences.

Ansirithm simply provides names for the machinery.

Because apparently `\033[36;1;4m` was considered a perfectly reasonable user interface.
