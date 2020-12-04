from arbol.arbol import lprint, lsection, section, Arbol

Arbol.max_depth = 4

lprint('Test')

@section('function')
def fun(x):
    if x >= 0:
        with lsection('recursive call to f'):
            lprint(f"f(x)+1={fun(x-1)}")

with lsection('a section'):
    lprint('a line')
    lprint('another line')
    lprint('we are done')

    with lsection('a subsection'):
        lprint('another line')
        lprint('we are done')

    fun(2)

    Arbol.elapsed_time = False
    fun(100)

lprint('test is finished...')


