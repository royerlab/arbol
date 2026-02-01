from arbol import Arbol, acapture, aprint, asection, section

# For colors: pip install arbol[colors]
# Or manually: pip install ansicolors colorama

# You can limit the tree depth:
Arbol.max_depth = 4

# use aprint (=arbol print) instead of the standard print
aprint('Test')


# You can decorate functions:
@section('function')
def fun(x):
    if x >= 0:
        with asection('recursive call to f'):
            aprint(f'f(x)+1={fun(x - 1)}')


# The context manager lets you go down one level in the tree
with asection('a section'):
    aprint('a line')
    aprint('another line')
    aprint('we are done \n or are we? \n someone gotta check!')

    with asection('a subsection'):
        aprint('another line')
        aprint('we are done')

    # works through function calls and the like...
    fun(2)

    # Capture stdout from third-party code (experimental):
    with acapture():
        print('No escape is possible')
        aprint('Even this works...\n')
        # Don't push it... you can't create subsections right now, might be possible in the future.

    # You can deactivate the elapsed time measurement and printing:
    Arbol.elapsed_time = False
    fun(100)

aprint('demo is finished...')

# You can also turn off all output with one switch:
Arbol.enable_output = False
aprint('you will not see that')
