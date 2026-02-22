import functools
import locale
import math
import sys
import time
from contextlib import contextmanager
from threading import local
from typing import Any

try:
    # for color support, install ansicolors
    from colors import color
except ImportError:

    def color(text: str, fg: str):
        return text


try:
    # For color support on windows:
    from colorama import init

    init(autoreset=True)
except ImportError:
    pass


class Arbol:
    """Configuration class for arborescent (tree-like) console output.

    All attributes are class-level and affect global behavior. Modify them
    directly to configure output formatting.

    Attributes
    ----------
    passthrough : bool
        If True, bypass tree formatting and use standard print (default: False).
    enable_output : bool
        If False, suppress all output (default: True).
    colorful : bool
        If True, apply ANSI colors when ansicolors is installed (default: True).
    max_depth : int | float
        Maximum tree depth to display. Deeper sections show truncation message
        (default: math.inf).
    elapsed_time : bool
        If True, show elapsed time for each section (default: True).

    Color Attributes
    ----------------
    c_text : str
        Hex color for regular text (default: '#2A9D8F').
    c_scaffold : str
        Hex color for tree lines (default: '#E9C46A').
    c_timing : str
        Hex color for elapsed time (default: '#2A9DAF').
    c_section : str
        Hex color for section headers (default: '#F4A261').
    c_truncation : str
        Hex color for truncation message (default: '#E76F51').

    Example
    -------
    >>> Arbol.max_depth = 3      # Limit tree depth
    >>> Arbol.elapsed_time = False  # Hide timing info
    >>> Arbol.colorful = False   # Disable colors
    """

    _depth = 0

    passthrough = False
    enable_output = True
    colorful = True
    max_depth = math.inf
    elapsed_time = True

    # Define colors:
    c_text = '#2A9D8F'
    c_scaffold = '#E9C46A'
    c_timing = '#2A9DAF'
    c_section = '#F4A261'
    c_truncation = '#E76F51'

    # Define special characters:
    _vl_ = '│'  # 'Vertical Line'
    _br_ = '├'  # 'Branch Right'
    _bd_ = '├╗'  # 'Branch Down'
    _tb_ = '┴'  # 'Terminate Branch'
    _la_ = '«'  # 'Left Arrow'

    #  Windows terminal is dumb. We can't use our fancy characters from Yesteryears, sad:
    if locale.getpreferredencoding() == 'US-ASCII' or locale.getpreferredencoding() == 'cp1252':
        _vl_ = '|'
        _br_ = '|->'
        _bd_ = '|\\'  # noqa: W605
        _tb_ = '-'
        _la_ = '<<'

    _thread_local = local()

    @staticmethod
    def native_print(text, *args, sep=' ', end='\n', file=None, flush=False):
        """Internal print function that respects enable_output setting."""
        if Arbol.enable_output:
            text = _colorise(text, fg=Arbol.c_text)
            args = (_colorise(arg, fg=Arbol.c_text) for arg in args)
            print(text, *args, sep=sep, end=end, file=file, flush=flush)

    @staticmethod
    def set_log_elapsed_time(log_elapsed_time: bool):
        """Enable or disable elapsed time display for sections.

        Parameters
        ----------
        log_elapsed_time : bool
            If True, show elapsed time after each section.
        """
        Arbol.elapsed_time = log_elapsed_time

    @staticmethod
    def set_log_max_depth(max_depth: int):
        """Set maximum tree depth for display.

        Parameters
        ----------
        max_depth : int
            Maximum number of visible section levels (1-indexed).
            For example, set_log_max_depth(2) shows 2 levels of sections.
            Values below 1 are clamped so that at least root-level
            aprint() output is visible.

        Note
        ----
        Internally stores max_depth - 1 because depth counting is 0-indexed.
        """
        Arbol.max_depth = max(0, max_depth - 1)


def _colorise(text: str, fg: str) -> str:
    """Apply color to text if Arbol.colorful is True and ansicolors is available."""
    if Arbol.colorful:
        return color(text, fg=fg)
    else:
        return text


def aprint(
    *args: Any, sep: str = ' ', end: str = '\n', file=None, flush: bool = False, separate_lines: bool = False
) -> None:
    """
    Arbol version of print. Drop-in replacement for the built-in print function.
    Text will be printed following the arborescent structure of sections.

    Parameters
    ----------
    *args : Any
        Values to print (same as built-in print).
    sep : str
        Separator between arguments (default: ' ').
    end : str
        String appended after the last value (default: '\\n').
    file : file-like object
        Output stream (default: sys.stdout).
    flush : bool
        Whether to forcibly flush the stream (default: False).
    separate_lines : bool
        Arbol-specific: display each line (\\n separated) as a separate branch in the tree.

    """

    if Arbol.passthrough or (hasattr(Arbol._thread_local, 'captured') and Arbol._thread_local.captured):
        print(*args, sep=sep, end=end, file=file, flush=flush)

    elif Arbol._depth <= Arbol.max_depth:
        level = min(Arbol.max_depth, Arbol._depth)
        text = sep.join(str(arg) for arg in args)
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if line:
                Arbol.native_print(
                    _colorise(
                        Arbol._vl_ * int(level) + (Arbol._br_ if i == 0 or separate_lines else Arbol._vl_),
                        fg=Arbol.c_scaffold,
                    )
                    + ' ',
                    end='',
                    file=file,
                )
                Arbol.native_print(line, sep=sep, end=end, file=file, flush=flush)


@contextmanager
def asection(section_header: str, file=None):
    """Context manager that creates a named section (node) in the output tree.

    All aprint() calls within this context are indented under the section header.
    Elapsed time is automatically measured and displayed when the section exits
    (unless Arbol.elapsed_time is False).

    Parameters
    ----------
    section_header : str
        The title displayed for this section in the tree.
    file : file-like object, optional
        Output stream (default: sys.stdout).

    Example
    -------
    >>> with asection('Processing data'):
    ...     aprint('Loading...')
    ...     with asection('Validation'):
    ...         aprint('Checking format')
    ...     aprint('Done')
    """

    if Arbol._depth + 1 <= Arbol.max_depth:
        Arbol.native_print(
            _colorise(Arbol._vl_ * Arbol._depth + Arbol._bd_, fg=Arbol.c_scaffold)
            + ' '
            + _colorise(section_header, fg=Arbol.c_section),
            file=file,
        )  # ≡
    elif Arbol._depth + 1 == Arbol.max_depth + 1:
        Arbol.native_print(
            _colorise(Arbol._vl_ * Arbol._depth + Arbol._br_ + '=', fg=Arbol.c_scaffold)
            + _colorise(f' {section_header}', fg=Arbol.c_section)
            + _colorise(' (log tree truncated here)', fg=Arbol.c_truncation),
            file=file,
        )

    Arbol._depth += 1

    start = time.time()
    exception = None
    try:
        yield
    except BaseException as e:
        exception = e

    stop = time.time()

    Arbol._depth -= 1
    if Arbol._depth <= Arbol.max_depth:
        if Arbol.elapsed_time:
            elapsed = stop - start
            _print_elapsed(elapsed, file)

        Arbol.native_print(_colorise(Arbol._vl_ * (Arbol._depth + 1), fg=Arbol.c_scaffold), file=file)

    if exception is not None:
        raise exception


def section(section_header: str, file=None):
    """Decorator that wraps a function in an asection context.

    Each call to the decorated function creates a section in the output tree.
    Useful for visualizing function call hierarchies.

    Parameters
    ----------
    section_header : str
        The title displayed for this section in the tree.
    file : file-like object, optional
        Output stream (default: sys.stdout).

    Example
    -------
    >>> @section('calculate')
    ... def calculate(x, y):
    ...     aprint(f'Computing {x} + {y}')
    ...     return x + y
    ...
    >>> result = calculate(2, 3)
    """

    def _outer(func):
        @functools.wraps(func)
        def _wrap(*args, **kwargs):
            with asection(section_header, file=file):
                return func(*args, **kwargs)

        return _wrap

    return _outer


@contextmanager
def acapture():
    """Context manager that captures stdout/stderr and redirects to arbol tree.

    Use this to integrate output from third-party libraries that use print()
    directly. The captured output is displayed through aprint() when the
    context exits.

    Warning
    -------
    This is experimental. Nested sections inside acapture() may not work
    correctly. Use sparingly and only when necessary.

    Example
    -------
    >>> with asection('External library'):
    ...     with acapture():
    ...         print('This comes from a library')  # Gets captured
    ...     aprint('Back to normal')
    """

    try:
        # Redirect
        import io

        sys.stdout = io.TextIOWrapper(io.BytesIO(), sys.stdout.encoding)
        sys.stderr = io.TextIOWrapper(io.BytesIO(), sys.stderr.encoding)

        Arbol._thread_local.captured = True
        try:
            yield
        finally:
            Arbol._thread_local.captured = False

    finally:
        # Read
        sys.stdout.seek(0)
        sys.stderr.seek(0)
        output_stdout = sys.stdout.read()
        output_stderr = sys.stderr.read()
        sys.stdout.close()
        sys.stderr.close()

        # Restore
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        # Send to arbol:
        aprint(output_stdout, separate_lines=True)
        aprint(output_stderr, file=sys.stderr, separate_lines=True)


def _print_elapsed(elapsed, file=None):
    """Print elapsed time in human-readable format (microseconds to days)."""
    if elapsed < 0.001:
        Arbol.native_print(
            _colorise(Arbol._vl_ * (Arbol._depth + 1) + Arbol._tb_ + Arbol._la_, fg=Arbol.c_scaffold)
            + _colorise(f' {elapsed * 1000 * 1000:.2f} microseconds', fg=Arbol.c_timing),
            file=file,
        )
    elif elapsed < 1:
        Arbol.native_print(
            _colorise(Arbol._vl_ * (Arbol._depth + 1) + Arbol._tb_ + Arbol._la_, fg=Arbol.c_scaffold)
            + _colorise(f' {elapsed * 1000:.2f} milliseconds', fg=Arbol.c_timing),
            file=file,
        )
    elif elapsed < 60:
        Arbol.native_print(
            _colorise(Arbol._vl_ * (Arbol._depth + 1) + Arbol._tb_ + Arbol._la_, fg=Arbol.c_scaffold)
            + _colorise(f' {elapsed:.2f} seconds', fg=Arbol.c_timing),
            file=file,
        )
    elif elapsed < 60 * 60:
        Arbol.native_print(
            _colorise(Arbol._vl_ * (Arbol._depth + 1) + Arbol._tb_ + Arbol._la_, fg=Arbol.c_scaffold)
            + _colorise(f' {elapsed / 60:.2f} minutes', fg=Arbol.c_timing),
            file=file,
        )
    elif elapsed < 24 * 60 * 60:
        Arbol.native_print(
            _colorise(Arbol._vl_ * (Arbol._depth + 1) + Arbol._tb_ + Arbol._la_, fg=Arbol.c_scaffold)
            + _colorise(f' {elapsed / (60 * 60):.2f} hours', fg=Arbol.c_timing),
            file=file,
        )
    else:
        Arbol.native_print(
            _colorise(Arbol._vl_ * (Arbol._depth + 1) + Arbol._tb_ + Arbol._la_, fg=Arbol.c_scaffold)
            + _colorise(f' {elapsed / (24 * 60 * 60):.2f} days', fg=Arbol.c_timing),
            file=file,
        )


# Legacy aliases (deprecated)
def lprint(*args, sep=' ', end='\n', file=None, flush=False):
    """Deprecated: Use aprint() instead."""
    return aprint(*args, sep=sep, end=end, file=file, flush=flush)


@contextmanager
def lsection(section_header: str, file=None):
    """Deprecated: Use asection() instead."""
    with asection(section_header, file=file):
        yield
