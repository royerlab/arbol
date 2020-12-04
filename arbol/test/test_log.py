from arbol.arbol import Arbol, lprint, lsection


def test_log():

    # This is required for this test to pass!
    Arbol.override_test_exclusion = True

    lprint('Test')

    with lsection('a section'):
        lprint('a line')
        lprint('another line')
        lprint('we are done')

        with lsection('a subsection'):
            lprint('another line')
            lprint('we are done')

            with lsection('a subsection'):
                lprint('another line')
                lprint('we are done')

                assert Arbol._depth == 3

                with lsection('a subsection'):
                    lprint('another line')
                    lprint('we are done')

                    with lsection('a subsection'):
                        lprint('another line')
                        lprint('we are done')

                        assert Arbol._depth == 5

                        with lsection('a subsection'):
                            lprint('another line')
                            lprint('we are done')

                            with lsection('a subsection'):
                                lprint('another line')
                                lprint('we are done')

                                assert Arbol._depth == 7

                        with lsection('a subsection'):
                            lprint('another line')
                            lprint('we are done')

                    with lsection('a subsection'):
                        lprint('another line')
                        lprint('we are done')

                with lsection('a subsection'):
                    lprint('another line')
                    lprint('we are done')

    lprint('test is finished...')

    assert Arbol._depth == 0
