# Ansirithm

**A little color. A little cursor control. Much less escape-code archaeology.**

Ansirithm is a lightweight Python utility for terminal styling, cursor control, screen manipulation, and text decoration. You get readable enums and a small sequence builder, so your application can say what it means without scattering mysterious escape strings through the code.

If you'd rather write this:

```python
Ansi.ansi(ForegroundColor.RED)
```

than remember that red is `31`, you're in the right place. The terminal can keep its secret numerical language; you can keep your afternoon.

[What it does](#what-it-does) · [Get started](#get-started) · [A quick example](#a-quick-example) · [How it fits together](#how-it-fits-together) · [Reference](#reference) · [Examples](#examples) · [Good to know](#good-to-know) · [Design notes](#design-notes)

## What it does

- Sets foreground colors with `ForegroundColor` and background colors with `BackgroundColor`.
- Applies bold, faint, and italic text through `Fonts`.
- Adds underlines, double underlines, strike-through, and overlines with `Decorators`.
- Builds blinking, reverse-video, and hidden-text effects through `Effects`.
- Moves the cursor, changes its visibility, and navigates between terminal lines.
- Erases the screen, scrollback, or part of a line.
- Sends the cursor home and saves or restores its position with `Teleportation`.
- Combines integer styling codes and string actions through `Ansi.ansi()`.
- Accepts reusable lists and tuples, ignores `None`, and returns an empty string for empty input.
- Resets text styling when a block ends through `Ansi.reset`, and supplies `Ansi.clear` for screen erasure followed by cursor home.

## Get started

> [!NOTE]
> Ansirithm uses only Python's standard library. It generates standard ANSI escape sequences; the receiving terminal is responsible for understanding and displaying them.

Import the classes you need from the module. Replace `ansirithm` with your installation's module path if it differs.

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

The main interface is:

```python
Ansi.ansi(*codes)
```

It accepts any number of style codes or action strings and returns a string. Write that string to terminal output to apply it; constructing the string alone does not change the terminal.

## A quick example

```python
print(
    Ansi.ansi(ForegroundColor.RED)
    + "Hello"
    + Ansi.ansi(Reset.RESET)
)
```

You get red `Hello` text followed by a style reset. That final reset keeps the next line from accidentally joining the red-text club.

You can apply more than one style in the same call:

```python
Ansi.ansi(
    ForegroundColor.RED,
    Fonts.BOLD
)
```

This combines the red foreground and bold font style into one styling sequence.

## How it fits together

### Styling codes and terminal actions

Ansirithm separates codes by the work they do:

| Kind | Input | What the builder emits |
| --- | --- | --- |
| Text styling | Integer SGR values: foreground colors, background colors, fonts, decorators, effects, and resets. | One combined SGR escape sequence. |
| Terminal actions | Strings for cursor movement, visibility, line navigation, erasing, and positioning. | A separate escape sequence for each action. |

SGR means Select Graphic Rendition: the ANSI mechanism for changing text attributes. The action commands use CSI, the Control Sequence Introducer used by these terminal operations.

When a call mixes styling and actions, the combined styling sequence comes first, followed by the action sequences in their string order. Integer styling values are joined with semicolons inside the single SGR sequence.

> [!TIP]
> Pass styling enum members directly to `Ansi.ansi()`. For terminal actions, pass the member's **`.value`**, as in `Ansi.ansi(CursorVisibility.SHOW.value)`. Ansirithm adds the escape prefix, so the action string contains the part after `ESC[`.

### Combine styles in one sequence

Pass several integer codes together when you want a reusable style:

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

All four values become one SGR sequence, conceptually:

```text
ESC[33;44;1;4m
```

The text follows that sequence, and the explicit reset ends the styling. You get yellow, bold, underlined text on a blue background without assembling the raw control string yourself.

### Reuse lists and tuples

`Ansi.ansi()` accepts lists and tuples as well as individual codes:

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

You can also combine a collection with individual arguments:

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

Lists and tuples are flattened **one level** before processing. That lets you keep a shared collection of theme values and add an extra decoration at the call site; it is not recursive flattening of arbitrarily deep collections.

### Leave optional styles as `None`

When a style is conditional, you can pass `None` for the unused part:

```python
color = ForegroundColor.RED
optional_style = None

sequence = Ansi.ansi(
    color,
    optional_style,
    Fonts.BOLD
)
```

The builder omits `optional_style` and keeps the red foreground and bold font. You don't need a separate formatting branch for every combination of optional attributes.

### Let empty input stay empty

Calling the builder without usable codes returns an empty string:

```python
Ansi.ansi()
```

Result:

```text
""
```

Empty collections and `None` behave the same way:

```python
Ansi.ansi(None, [], ())
```

This also produces `""`, so an empty style can safely participate in string concatenation without special handling.

### Reset styling when a block ends

The reset helper is exposed through:

```python
Ansi.reset
```

Use the context manager with the callable form shown here:

```python
with Ansi.reset():
    print("Styled output")
```

Its `__enter__()` method returns `Ansi.ansi`, so you can bind the sequence builder to a local name:

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

When the context exits, it prints the reset sequence automatically:

```text
ESC[0m
```

That restores the default text styling after temporary formatting. The plain `"Styled output"` example shows the context-manager structure; the second example actually applies a style inside it.

> [!IMPORTANT]
> A text reset restores **text attributes**. It does not show a hidden cursor or restore its position. Pair cursor hiding with `CursorVisibility.SHOW.value` when you're finished; a `finally` block is useful when the intervening work can raise an exception.

### Clear the screen and go home

Use the predefined clear sequence:

```python
Ansi.clear
```

Conceptually, it contains these two commands:

```text
ESC[2J ESC[H
```

Write it without adding a newline:

```python
print(Ansi.clear, end="")
```

This first erases the screen and then moves the cursor to the home position. In Python string notation, the combined sequence is `"\x1b[2J\x1b[H"`.

## Reference

### Foreground colors

`ForegroundColor` supplies the eight standard ANSI foreground colors. Pass these enum members directly to the builder.

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

For a red message:

```python
print(
    Ansi.ansi(ForegroundColor.RED)
    + "Red text"
    + Ansi.ansi(Reset.RESET)
)
```

For bold green text:

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

The foreground color stays active until another style sequence changes it or a reset clears it. Terminals appreciate a clear ending.

### Background colors

`BackgroundColor` supplies the corresponding eight background colors:

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

Set a blue background:

```python
print(
    Ansi.ansi(BackgroundColor.BLUE)
    + "Blue background"
    + Ansi.ansi(Reset.RESET)
)
```

Or combine it with a white foreground:

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

### Fonts

`Fonts` supplies common text-style attributes:

| Style | ANSI Code |
|---|---:|
| `BOLD` | `1` |
| `FAINT` | `2` |
| `ITALIC` | `3` |

Apply bold text:

```python
print(
    Ansi.ansi(Fonts.BOLD)
    + "Bold text"
    + Ansi.ansi(Reset.RESET)
)
```

Or request several font attributes together:

```python
Ansi.ansi(
    Fonts.BOLD,
    Fonts.ITALIC
)
```

> [!NOTE]
> Individual styles depend on the terminal emulator. Faint and italic text, in particular, may look different or be unsupported. ANSI has a standard; terminals still bring their own opinions.

### Text decorators

`Decorators` covers these text decorations:

| Decorator | ANSI Code |
|---|---:|
| `UNDERLINE` | `4` |
| `DOUBLE_UNDERLINE` | `21` |
| `STRIKE` | `9` |
| `OVERLINE` | `53` |

Underline a message:

```python
print(
    Ansi.ansi(Decorators.UNDERLINE)
    + "Underlined text"
    + Ansi.ansi(Reset.RESET)
)
```

Or combine a decorator with a color and font style:

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

### Terminal effects

`Effects` supplies blinking, reverse video, and hidden text:

| Effect | ANSI Code |
|---|---:|
| `BLINK` | `5` |
| `REVERSE` | `7` |
| `HIDDEN` | `8` |

For reverse video:

```python
print(
    Ansi.ansi(Effects.REVERSE)
    + "Reverse video"
    + Ansi.ansi(Reset.RESET)
)
```

Blinking depends on terminal support. `HIDDEN` is commonly used to conceal terminal text, but the receiving terminal still decides how that effect behaves.

### Reset

`Reset` currently has one member:

| Operation | ANSI Code |
|---|---:|
| `RESET` | `0` |

Use it to return text styling to its default state:

```python
print(
    Ansi.ansi(ForegroundColor.RED)
    + "Red"
    + Ansi.ansi(Reset.RESET)
    + " Normal"
)
```

The reset stops your styling from leaking into later output, which matters especially when your code is part of a reusable terminal application.

### Cursor movement

`CursorMovement` provides directional CSI commands:

| Direction | ANSI Command |
|---|---|
| `UP` | `A` |
| `DOWN` | `B` |
| `RIGHT` | `C` |
| `LEFT` | `D` |

For example:

```python
print(
    Ansi.ansi(
        CursorMovement.UP.value
    )
)
```

The enum value supplies the direction without a distance. When the numeric parameter is omitted, the terminal applies the ANSI default. You can build a parameterized action string, such as `f"2{CursorMovement.UP.value}"`, to request two rows explicitly.

### Cursor visibility

`CursorVisibility` lets you hide or show the cursor:

| Operation | ANSI Sequence |
|---|---|
| `HIDE` | `?25l` |
| `SHOW` | `?25h` |

Hide it:

```python
print(
    Ansi.ansi(
        CursorVisibility.HIDE.value
    ),
    end=""
)
```

Show it again:

```python
print(
    Ansi.ansi(
        CursorVisibility.SHOW.value
    ),
    end=""
)
```

This is useful for terminal interfaces, animations, and progress displays where a blinking cursor would otherwise wander through the scenery.

### Line navigation

`LineNavigation` provides commands for moving between terminal lines:

| Operation | ANSI Command |
|---|---|
| `NEXT` | `E` |
| `PREV` | `F` |

For example:

```python
print(
    Ansi.ansi(
        LineNavigation.NEXT.value
    )
)
```

`Ansi.ansi()` emits these as CSI sequences. `NEXT` moves to the start of a following line and `PREV` to the start of a preceding line; a numeric prefix supplies the count.

### Erasing

`Erasing` removes terminal content:

| Operation | ANSI Command |
|---|---|
| `SCREEN` | `2J` |
| `SCROLL` | `3J` |
| `LINE` | `K` |
| `TO_START` | `1K` |

| Member | Area affected |
| --- | --- |
| `SCREEN` | The screen. |
| `SCROLL` | Scrollback. |
| `LINE` | From the cursor to the end of the current line. |
| `TO_START` | From the start of the current line to the cursor. |

Clear the screen:

```python
print(
    Ansi.ansi(
        Erasing.SCREEN.value
    ),
    end=""
)
```

Clear the rest of the current line:

```python
print(
    Ansi.ansi(
        Erasing.LINE.value
    ),
    end=""
)
```

Clear back to the start of the line:

```python
print(
    Ansi.ansi(
        Erasing.TO_START.value
    ),
    end=""
)
```

These actions let you update visible output without treating every change as another printed line.

> [!TIP]
> Erasing a line does not move the cursor to its beginning. Combine erasing with cursor movement when you need both. `Ansi.clear` requests screen erasure and home, while `Erasing.SCROLL` is a separate scrollback operation.

### Teleportation

`Teleportation` groups cursor positioning and position-storage commands. No science-fiction equipment required.

| Operation | ANSI Command |
|---|---|
| `HOME` | `H` |
| `SAVE` | `s` |
| `RESTORE` | `u` |

Move to the terminal's home position:

```python
print(
    Ansi.ansi(
        Teleportation.HOME.value
    ),
    end=""
)
```

Save the current cursor position:

```python
print(
    Ansi.ansi(
        Teleportation.SAVE.value
    ),
    end=""
)
```

Restore the saved position:

```python
print(
    Ansi.ansi(
        Teleportation.RESTORE.value
    ),
    end=""
)
```

Saving and restoring is useful when you temporarily write somewhere else and then return to the previous cursor location. Support for position save/restore can vary between terminals.

### API at a glance

The complete member list is below. For the action enums, use `.value` when passing a member to `Ansi.ansi()`.

#### Foreground Colors

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

#### Background Colors

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

#### Fonts

```python
Fonts.BOLD
Fonts.FAINT
Fonts.ITALIC
```

#### Decorators

```python
Decorators.UNDERLINE
Decorators.DOUBLE_UNDERLINE
Decorators.STRIKE
Decorators.OVERLINE
```

#### Effects

```python
Effects.BLINK
Effects.REVERSE
Effects.HIDDEN
```

#### Reset

```python
Reset.RESET
```

#### Cursor Movement

```python
CursorMovement.UP
CursorMovement.DOWN
CursorMovement.RIGHT
CursorMovement.LEFT
```

#### Cursor Visibility

```python
CursorVisibility.HIDE
CursorVisibility.SHOW
```

#### Line Navigation

```python
LineNavigation.NEXT
LineNavigation.PREV
```

#### Erasing

```python
Erasing.SCREEN
Erasing.SCROLL
Erasing.LINE
Erasing.TO_START
```

#### Teleportation

```python
Teleportation.HOME
Teleportation.SAVE
Teleportation.RESTORE
```

#### Main Interface

```python
Ansi.ansi(*codes)
Ansi.reset
Ansi.clear
```

## Examples

### Styled terminal output

This combines foreground colors, background colors, fonts, decorations, and explicit resets:

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

The workflow is straightforward: construct a style, print the text, reset the style, and continue with normal output. The cursor-control example is separate below.

### Cursor control

This example hides the cursor, erases the screen, moves home, prints a message, and restores visibility:

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

It shows the basic building blocks for a simple terminal interface or screen-based application. If you add work that can fail between `HIDE` and `SHOW`, put the visibility restoration in a `finally` block.

### Dynamic styling and reusable themes

Collections and optional values let you assemble a style dynamically:

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

Here, `Ansi.ansi(0)` uses the numeric SGR reset value directly. `Ansi.ansi(Reset.RESET)` expresses the same reset with a readable enum name.

You can also build named styles once and reuse them throughout an application:

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

### A compact greeting

For a small program, the same pattern fits comfortably in one place:

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

Visible text:

```text
Hello from Ansirithm
```

The terminal applies the cyan foreground, bold font, and underline from the emitted ANSI sequences. The plain-text output above shows the characters, not their visual formatting.

## Good to know

> [!IMPORTANT]
> Ansirithm generates sequences; it does not check the receiving terminal's capabilities or disable ANSI automatically. Redirected output still contains those sequences, so choose when to add styling if the same output also goes to a file.

The current implementation covers a subset of ANSI terminal functionality. It does not provide:

- 256-color support.
- True-color RGB sequences.
- A dedicated arbitrary row-and-column cursor-positioning interface.
- Terminal input handling.
- Keyboard event parsing.
- Terminal size detection.
- Platform-specific console APIs.
- Automatic terminal capability detection.
- Automatic ANSI disabling for unsupported terminals.
- Full ANSI/ECMA-48 sequence coverage.

Effect support varies between terminal emulators, especially for blinking, faint text, double underlines, overlines, and cursor-position save/restore. The library does not verify that a requested effect is supported.

## Design notes

Ansirithm keeps terminal control explicit. Named enums make the codes readable, and `Ansi.ansi()` is the shared mechanism that turns those values into actual escape strings.

Each category has a specific job: `ForegroundColor` and `BackgroundColor` select colors; `Fonts`, `Decorators`, and `Effects` set text attributes; `Reset` ends those attributes; `CursorMovement`, `CursorVisibility`, and `LineNavigation` control the cursor; `Erasing` removes content; and `Teleportation` handles home, save, and restore operations.

The utility stays focused on that translation layer rather than implementing a terminal emulator. You retain the ANSI control system, with readable names attached to the machinery. A respectable improvement over treating `\033[36;1;4m` as a friendly user interface.
