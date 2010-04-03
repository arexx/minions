


def name(minion, inp):
    """Requires that the message include the minion's name somewhere."""
    print "REQUIRE.NAME: Looking for %s in %s" % (minion.nick.upper(), inp)
    return inp.find(minion.nick.upper()) > -1