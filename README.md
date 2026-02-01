# arbol | Arborescent Printouts in Python

![s](arbol.png)

Do you have a script, a command line tool, or some workflow in Python that has lots of `print` statements, and you can't make sense of it once it adds up to hundreds of lines on the console? Sounds familiar?

**arbol** organizes your stdout prints in a hierarchy that follows the structure of your code. Use a simple context manager to define the hierarchy and `aprint` instead of `print`, and voila. When the optional dependencies are installed, the output is colored with an exquisitely crafted combination of colors, making it even more visually appealing.

If you are wondering, *arbol* means *tree* in Spanish.

Why not use traditional Python logging? We made the choice of sticking to a plain and simple scheme that matches the usage of `print` statements.

## Features

- **`aprint`**: Drop-in replacement for the built-in `print` function
- **`asection`**: Context manager to create tree nodes with automatic timing
- **`section`**: Decorator to wrap functions in a section
- **`acapture`**: Context manager to capture stdout/stderr from third-party code
- **Configuration**: Control depth, colors, timing display via `Arbol` class

## Installation

Install with pip:

```sh
pip install arbol
```

Or with optional color support:

```sh
pip install arbol[colors]
```

## Optional Dependencies

For colors, install the [ansicolors](https://pypi.org/project/ansicolors/) package:

```sh
pip install ansicolors
```

For color support on all operating systems (particularly Windows), install [colorama](https://pypi.org/project/colorama/):

```sh
pip install colorama
```

Note: both are optional — arbol works fine without them.

## Example

```python
from arbol import Arbol, aprint, section, asection, acapture

# Limit the tree depth:
Arbol.max_depth = 4

# Use aprint instead of print
aprint('Test')

# Decorate functions to wrap them in a section:
@section('function')
def fun(x):
    if x >= 0:
        with asection('recursive call'):
            aprint(f"f(x)+1={fun(x - 1)}")

# Context manager lets you go down one level in the tree:
with asection('a section'):
    aprint('a line')
    aprint('another line')
    aprint('we are done \n or are we? \n someone gotta check!')

    with asection('a subsection'):
        aprint('another line')
        aprint('we are done')

    # Works through function calls:
    fun(2)

    # Capture stdout from third-party code (experimental):
    with acapture():
        print("This gets captured")

    # Disable elapsed time display:
    Arbol.elapsed_time = False
    fun(100)

aprint('demo is finished...')

# Turn off all output:
Arbol.enable_output = False
aprint('you will not see this')
```

Output:

![example](example.png)

## Configuration

All settings are class attributes on `Arbol`:

| Attribute | Default | Description |
|-----------|---------|-------------|
| `enable_output` | `True` | Set to `False` to suppress all output |
| `elapsed_time` | `True` | Set to `False` to hide timing information |
| `max_depth` | `math.inf` | Maximum tree depth (deeper sections show truncation) |
| `colorful` | `True` | Set to `False` to disable colors |
| `passthrough` | `False` | Set to `True` to bypass tree formatting entirely |

Color attributes (`c_text`, `c_scaffold`, `c_timing`, `c_section`, `c_truncation`) can also be customized with hex color codes.

## Roadmap

Ideas we might consider, from serious to speculative:

- More color styles to choose from
- Intercept stdout from C code so that printouts from native libraries are formatted too (unclear if possible)
- Generate tree automatically by inspecting stack
- Interoperability with the logging package
- Better multi-thread/process support — currently printouts get interleaved. One idea: capture outputs per-thread and display them in order when done.

## Development

```sh
make install    # Install hatch and set up environment
make test       # Run tests
make demo       # Run the demo
make lint       # Run linter (ruff)
make format     # Format code (ruff)
make check      # Run all checks (lint + format)
make publish    # Bump version and release
```

## Contributions

Pull requests welcome!

## Authors

- Loic A. Royer ([@loicaroyer](https://twitter.com/loicaroyer))
- Ahmet Can Solak ([@_ahmetcansolak](https://twitter.com/_ahmetcansolak))
