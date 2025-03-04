from arbol.arbol import Arbol, aprint, asection


def test_arbol():

    aprint('Test')

    with asection('a section'):
        aprint('a line')
        aprint('another line')
        aprint('we are done')

        with asection('a subsection'):
            aprint('another line')
            aprint('we are done')

            with asection('a subsection'):
                aprint('another line')
                aprint('we are done')

                assert Arbol._depth == 3

                with asection('a subsection'):
                    aprint('another line')
                    aprint('we are done')

                    with asection('a subsection'):
                        aprint('another line')
                        aprint('we are done')

                        assert Arbol._depth == 5

                        with asection('a subsection'):
                            aprint('another line')
                            aprint('we are done')

                            with asection('a subsection'):
                                aprint('another line')
                                aprint('we are done')

                                assert Arbol._depth == 7

                        with asection('a subsection'):
                            aprint('another line')
                            aprint('we are done')

                    with asection('a subsection'):
                        aprint('another line')
                        aprint('we are done')

                with asection('a subsection'):
                    aprint('another line')
                    aprint('we are done')

    aprint('test is finished...')

    assert Arbol._depth == 0

def test_arbol_exception_handling():
    try:
        with asection('a section with exception'):
            aprint('This will raise an exception')
            raise ValueError('An error occurred')
    except ValueError as e:
        assert str(e) == 'An error occurred'
    else:
        assert False, "Exception was not raised"