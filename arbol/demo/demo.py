from arbol.arbol import aprint, asection, section, Arbol

# for colors, install the ansicolors package: 'pip install ansicolors',
# and for windows install the colorama package: 'pip install colorama'

# You can limit the tree depth:
Arbol.max_depth = 4

# use lprint instead of the standard print
aprint('Test')

# You can decorate functions:
@section('function')
def fun(x):
    if x >= 0:
        with asection('recursive call to f'):
            aprint(f"f(x)+1={fun(x - 1)}")

# The context manager let's you start a 'section' i.e. a node in the tree
with asection('a section'):
    aprint('a line')
    aprint('another line')
    aprint('we are done')

    with asection('a subsection'):
        aprint('another line')
        aprint('we are done')

    fun(2)

    # You can deactivate the elapsed time measurement and printing:
    Arbol.elapsed_time = False
    fun(100)

aprint('demo is finished...')

# You can also turn off all output with one switch:
Arbol.enable_output = False
aprint('you will not see that')


