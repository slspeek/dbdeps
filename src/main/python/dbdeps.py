from graphviz import Digraph
# get the uno component context from the PyUNO runtime


def sleep(s):
    import time
    time.sleep(0.5 * s)


def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]


def fromPart(query):
    i = query.split(" FROM ")
    return ((i[-1].split(" WHERE "))[0].split(" ORDER BY "))[0]


class DBDeps(object):

    def __init__(self, datasource):
        self.datasource = datasource
        self.tables = datasource.Tables
        self.c = datasource.getConnection('sa', '')
        self.dbdoc = datasource.DatabaseDocument
        self.forms = self.dbdoc.FormDocuments
        self.reports = self.dbdoc.ReportDocuments

    def tableNames(self):
        return diff(list(self.tables.ElementNames), list(self.c.Views.ElementNames))

    def views(self):
        return self.c.Views.ElementNames

    def queries(self):
        return self.datasource.getQueryDefinitions();

    def buildGraph(self):
        g = Digraph('G', filename='dbdeps.gv')
        g.attr('graph', rankdir='LR')
        with g.subgraph(name='tables') as t:
            # t.attr(rank='same')
            t.attr('node', shape='rectangle')
            for n in self.tableNames():
                t.node(n)
        with g.subgraph(name='views') as v:
            v.attr('edge', arrowhead='dot')
            v.attr('node', shape='trapezium')
            for n in self.views():
                v.node(n)
                view = self.c.Views.getByName(n)
                fr = fromPart(view.Command)
                for t in self.tableNames():
                    if fr.find(t) > 0:
                        v.edge(n, t)
        with g.subgraph(name='queries') as q:
            self.subg_queries(q)
        with g.subgraph(name='forms') as f:
            f.attr('node', shape='rect', style='filled', fillcolor='#ffcc99')
            for i in self.forms.ElementNames:
                f.node(i)
        g.view()

    def subg_queries(self, sub):
        for query in self.queries().ElementNames:
            sub.node(query)


def buildGraph(datasource):
    dbdeps = DBDeps(datasource)
    dbdeps.buildGraph()





def graph():
    try:
        db = XSCRIPTCONTEXT.getDocument().DataSource
    except AttributeError:
        from apso_utils import msgbox
        msgbox("No database file open")
        return

    buildGraph(db)


def consoleDlg():
    ctx = XSCRIPTCONTEXT.getComponentContext()
    smgr = ctx.getServiceManager()
    dp = smgr.createInstanceWithContext("com.sun.star.awt.DialogProvider", ctx)
    dlg = dp.createDialog("vnd.sun.star.script:Access2Base.dlgTrace?location=application")
    dlg.execute()
    dlg.dispose()




# def magic(f):
#     c = f.open()
#     sleep(2)
#     print(f.Name, c.DrawPage.Forms[0].Command)
#     rec_magic(c.DrawPage.Forms[0])
#     f.close()
# 
# 
# def rec_magic(form):
#     for i in form:
#         # print("Control name", i.Name)
#         if i.getServiceName() == 'stardiv.one.form.component.ListBox':
#             if (str(i.ListSourceType)).find('QUERY') > -1:
#                 print(i.ListSource)
#         if i.getServiceName() == 'stardiv.one.form.component.Form':
#             print('subform', i.Command)
#             rec_magic(i)
# 
# 
# def report(r):
#     c = r.openDesign()
#     sleep(2)
#     print(r.Name, r.Component.Command)
#     r.close()
# 
# 
# def formDemo():
#     for f in forms:
#         print(f.Name)
#         magic(f)
# 
# 
# def reportDemo():
#     for r in reports:
#         report(r)

# if __name__ == 'main':
#     import uno
#     localContext = uno.getComponentContext()
# 
#     # create the UnoUrlResolver
#     resolver = localContext.ServiceManager.createInstanceWithContext(
#                     "com.sun.star.bridge.UnoUrlResolver", localContext)
# 
#     # connect to the running office
#     ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
#     smgr = ctx.ServiceManager
# 
#     def datasource():
#         return smgr.createInstance("com.sun.star.sdb.DatabaseContext").getByName("ona-ledenlijst")
# 
#     buildGraph(datasource())


g_exportedScripts = (graph,)
