import locale
import math
import sys
import time
from contextlib import contextmanager

try:
    # for color support, install ansicolors
    from colors import color
except ImportError:
    def color(text: str, fg: str):
        return text


class Arbol:
    """ Arborescent (Hierarchical) Logging.
        Python package to organise your stdout prints
        in a hierarchy that follows the structure of your code.
    """

    _depth = 0

    # current_section = ''
    enable_output = True
    colorful = True
    max_depth = math.inf
    elapsed_time = True

    # Define colors:
    c_text = '#2A9D8F'
    c_scafold = '#E9C46A'
    c_timming = '#2A9DAF'
    c_section = '#F4A261'
    c_truncat = '#E76F51'

    # Define special characters:
    _vl_ = '│'  # 'Vertical Line'
    _br_ = '├'  # 'Branch Right'
    _bd_ = '├╗'  # 'Branch Down'
    _tb_ = '┴'  # 'Terminate Branch'
    _la_ = '«'  # 'Left Arrow'

    #  Windows terminal is dumb. We can't use our fancy characters from Yesteryears, sad:
    if (
            locale.getpreferredencoding() == "US-ASCII"
            or locale.getpreferredencoding() == "cp1252"
    ):
        _vl_ = '|'
        _br_ = '|->'
        _bd_ = '|\\'  # noqa: W605
        _tb_ = '-'
        _la_ = '<<'

    def __init__(self):
        return

    @staticmethod
    def native_print(*args, sep=' ', end='\n', file=sys.__stdout__):
        if Arbol.enable_output:
            args = (_colorise(arg, fg=Arbol.c_text) for arg in args)
            print(*args, sep=sep, end=end, file=file)

    def set_log_elapsed_time(log_elapsed_time: bool):
        Arbol.elapsed_time = log_elapsed_time

    def set_log_max_depth(max_depth: int):
        Arbol.max_depth = max(0, max_depth - 1)


def _colorise(text: str, fg: str):
    if Arbol.colorful:
        return color(text, fg=fg)
    else:
        return text


def aprint(*args, sep=' ', end='\n'):
    """
    Arbol version of print. Text will be printed following the arborescent structure of sections.

    Parameters
    ----------
    args : list
    sep : str
    end : str

    """

    if Arbol._depth <= Arbol.max_depth:
        level = min(Arbol.max_depth, Arbol._depth)
        text = sep.join(tuple(str(arg) for arg in args))+end
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if line:
                Arbol.native_print(_colorise(Arbol._vl_ * int(level) + (Arbol._br_ if i == 0 else Arbol._vl_), fg=Arbol.c_scafold) + ' ', end='')
                Arbol.native_print(line, sep=sep, end='\n')


@contextmanager
def asection(section_header: str):
    """
    Introduces a 'node' in the tree below which context-bound 'aprints' will be placed.
    Ideally, you want to carefully choose blocks of code / workflow units so that it forms a 'unit'.

    Parameters
    ----------
    section_header : section header

    """

    if Arbol._depth + 1 <= Arbol.max_depth:
        Arbol.native_print(
            _colorise(Arbol._vl_ * Arbol._depth + Arbol._bd_, fg=Arbol.c_scafold)
            + ' ' + _colorise(section_header, fg=Arbol.c_section)
        )  # ≡
    elif Arbol._depth + 1 == Arbol.max_depth + 1:
        Arbol.native_print(
            _colorise(Arbol._vl_ * Arbol._depth
                      + Arbol._br_ + '=', fg=Arbol.c_scafold)
            + _colorise(f' {section_header}', fg=Arbol.c_section) + color(' (log tree truncated here)', fg=Arbol.c_truncat)
        )

    Arbol._depth += 1

    start = time.time()
    exception = None
    try:
        yield
    except Exception as e:
        exception = e

    stop = time.time()

    Arbol._depth -= 1
    if Arbol._depth + 1 <= Arbol.max_depth:

        if Arbol.elapsed_time:
            elapsed = stop - start
            _print_elapsed(elapsed)

        Arbol.native_print(_colorise(Arbol._vl_ * (Arbol._depth + 1), fg=Arbol.c_scafold))

        if exception is not None:
            raise exception


def section(section_header: str):
    """
    Function decorator that initiates a section for each function call.
    Don't abuse this too much or you might pollute your stack trace excessively...

    Parameters
    ----------
    section_header : section header

    """

    def _outer(func):
        def _wrap(*args, **kwargs):
            with asection(section_header):
                return func(*args, **kwargs)

        return _wrap

    return _outer


def _print_elapsed(elapsed):
    if elapsed < 0.001:
        Arbol.native_print(
            _colorise(Arbol._vl_ * (Arbol._depth + 1)
                      + Arbol._tb_
                      + Arbol._la_, fg=Arbol.c_scafold)
            + _colorise(f' {elapsed * 1000 * 1000:.2f} microseconds', fg=Arbol.c_timming)
        )
    elif elapsed < 1:
        Arbol.native_print(
            _colorise(Arbol._vl_ * (Arbol._depth + 1)
                      + Arbol._tb_
                      + Arbol._la_, fg=Arbol.c_scafold)
            + _colorise(f' {elapsed * 1000:.2f} milliseconds', fg=Arbol.c_timming)
        )
    elif elapsed < 60:
        Arbol.native_print(
            _colorise(Arbol._vl_ * (Arbol._depth + 1)
                      + Arbol._tb_
                      + Arbol._la_, fg=Arbol.c_scafold)
            + _colorise(f' {elapsed:.2f} seconds', fg=Arbol.c_timming)
        )
    elif elapsed < 60 * 60:
        Arbol.native_print(
            _colorise(Arbol._vl_ * (Arbol._depth + 1)
                      + Arbol._tb_
                      + Arbol._la_, fg=Arbol.c_scafold)
            + _colorise(f' {elapsed / 60:.2f} minutes', fg=Arbol.c_timming)
        )
    elif elapsed < 24 * 60 * 60:
        Arbol.native_print(
            _colorise(Arbol._vl_ * (Arbol._depth + 1)
                      + Arbol._tb_
                      + Arbol._la_, fg=Arbol.c_scafold)
            + _colorise(f' {elapsed / (60 * 60):.2f} hours', fg=Arbol.c_timming)
        )


# Some legacy projects are using previous function names, this is deprecated!
def lprint(*args, sep=' ', end='\n'):
    return lprint(*args, sep=sep, end=end)

def lsection(section_header: str):
    with asection(section_header):
        yield
