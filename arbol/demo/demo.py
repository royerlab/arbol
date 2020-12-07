from arbol import Arbol, aprint, section, asection, acapture

import arbol

# for colors, install the ansicolors package: 'pip install ansicolors',
# and for windows install the colorama package: 'pip install colorama'

# You can limit the tree depth:
Arbol.max_depth = 4

# use aprint (=arbol print) instead of the standard print
aprint('Test')

# You can decorate functions:
@section('function')
def fun(x):
    if x >= 0:
        with asection('recursive call to f'):
            aprint(f"f(x)+1={fun(x - 1)}")

# The context manager let's you go down one level in the tree
with asection('a section'):
    aprint('a line')
    aprint('another line')
    aprint('we are done \n or are we? \n someone gotta check!')

    with asection('a subsection'):
        aprint('another line')
        aprint('we are done')

    # works through function calls and the like...
    fun(2)

    # You can capture stdout if you want, usefull when a 3rd party library has printouts that you want to capture...
    with acapture():
        print("No escape is possible")
        aprint("Even this works...\n")

    # You can deactivate the elapsed time measurement and printing:
    Arbol.elapsed_time = False
    fun(100)

aprint('demo is finished...')

# You can also turn off all output with one switch:
Arbol.enable_output = False
aprint('you will not see that')


