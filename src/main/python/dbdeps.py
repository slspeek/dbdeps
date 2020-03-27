import socket  # only needed on win32-OOo3.0.0
import uno
from graphviz import Digraph
# get the uno component context from the PyUNO runtime
localContext = uno.getComponentContext()

# create the UnoUrlResolver
resolver = localContext.ServiceManager.createInstanceWithContext(
				"com.sun.star.bridge.UnoUrlResolver", localContext )

# connect to the running office
ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
smgr = ctx.ServiceManager

def datasouce():
    return smgr.createInstance("com.sun.star.sdb.DatabaseContext").getByName("ona-ledenlijst")

db = datasouce()

forms = db.DatabaseDocument.FormDocuments

tables = db.getTables()

reports = db.DatabaseDocument.ReportDocuments

c = db.getConnection('sa','')

def fromPart(query):
    i = query.split(" FROM ")
    return ((i[-1].split(" WHERE "))[0].split(" ORDER BY "))[0]

def queries():
    return datasouce().getQueryDefinitions();

def lijst():
    for q in queries():
        print(q.Name, fromPart(q.Command))

def sleep(s):
    import time
    time.sleep(0.5 * s)

def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]


def magic(f):
    c = f.open()
    sleep(2)
    print(f.Name, c.DrawPage.Forms[0].Command)
    rec_magic(c.DrawPage.Forms[0])
    f.close()

def rec_magic(form):
    for i in form:
        #print("Control name", i.Name)
        if i.getServiceName() == 'stardiv.one.form.component.ListBox':
             if (str(i.ListSourceType)).find('QUERY') > -1:
                print(i.ListSource)
        if i.getServiceName() == 'stardiv.one.form.component.Form':
            print('subform', i.Command)
            rec_magic(i)

def report(r):
    c = r.openDesign()
    sleep(2)
    print(r.Name, r.Component.Command)
    r.close()

def formDemo():
    for f in forms:
        print(f.Name)
        magic(f)

def reportDemo():
    for r in reports:
        report(r)

f = forms.getByName('Aspirant kiezen voor brief')
f2 = forms.getByName("Lid wijzigen")

r = reports.getByName('gadresboek')

def tableNames():
    return diff(list(c.Tables.ElementNames),list(c.Views.ElementNames))

def views():
    return c.Views.ElementNames

def buildGraph():
    g = Digraph('G', filename='dbdeps.gv')
    g.attr('graph', rankdir='LR')
    with g.subgraph(name='tables') as t:
        #t.attr(rank='same')
        t.attr('node', shape='rectangle')
        for n in tableNames():
            t.node(n)

    with g.subgraph(name='views') as v:
        #v.attr(rank='same')
        v.attr('node', shape='trapezium')
        for n in views():
            v.node(n)
            view = c.Views.getByName(n)
            fr = fromPart(view.Command)
            for t in tableNames():
                if fr.find(t) > 0:
                    v.edge(n, t)

    with g.subgraph(name='queries') as q:
        for query in queries().getElementNames():
            q.node(query)

    with g.subgraph(name='forms') as f:
        f.attr('node', shape='rect', style='filled', fillcolor='#ffcc99')
        for i in forms.getElementNames():
            f.node(i)
    g.view()

if __name__ == "__main__":
    # execute only if run as a script
    buildGraph()
