import collections


View = collections.namedtuple('View', 'name cmd')
Key = collections.namedtuple('Key', 'name columns referenced_table type')
Table = collections.namedtuple('Table', 'name keys')
Query = collections.namedtuple('Query', 'name cmd')


def tables(con):
    ts = []
    for t in con.Tables:
        if t.Type == 'TABLE':
            keys = []
            for k in t.Keys:
                k = Key(name=k.Name,
                        columns=list(k.Columns.ElementNames),
                        referenced_table=k.ReferencedTable,
                        type=k.Type)
                keys.append(k)
            mytable = Table(name=t.Name, keys=keys)
            ts.append(mytable)
    return ts


def views(con):
    vs = []
    for v in con.Views:
        v = View(name=v.Name, cmd=v.Command)
        vs.append(v)
    return vs


def queries(ds):
    return [Query(name=q.Name, cmd=q.Command) for q in ds.QueryDefinitions]
