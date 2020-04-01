def fromPart(query):
    i = query.split(" FROM ")
    return ((i[-1].split(" WHERE "))[0].split(" ORDER BY "))[0]


def contains(string, substr):
    sub = '"{0}"'.format(substr)
    return sub in string


def refers(cmd, name):
    s = fromPart(cmd)
    return contains(s, name)
