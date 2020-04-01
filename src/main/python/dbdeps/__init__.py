from graphviz import Digraph
# get the uno component context from the PyUNO runtime
from dbdeps.table import *
from dbdeps.open_helper import *
from dbdeps.sql_helper import refers
import os
import uno
getConstantByName = uno.pyuno.getConstantByName

def nnt(name):
    return 'table_{0}'.format(name)


def nnv(name):
    return 'view_{0}'.format(name)


def nnq(name):
    return 'query_{0}'.format(name)


TABLE_TYPE = getConstantByName('com.sun.star.sdb.CommandType.TABLE')
QUERY_TYPE = getConstantByName('com.sun.star.sdb.CommandType.QUERY')
COMMAND_TYPE = getConstantByName('com.sun.star.sdb.CommandType.COMMAND')


class DBDeps(object):

    def __init__(self, datasource):
        self.c = datasource.getConnection('sa', '')
        self.datasource = datasource
        self.tables = tables(self.c)
        self.views = views(self.c)
        self.queries = queries(self.datasource)
        self.dbdoc = datasource.DatabaseDocument
        self.forms = self.dbdoc.FormDocuments
        self.reports = self.dbdoc.ReportDocuments

    def depends(self, g,  name, nnaming, cmd, series, snaming):
        for i in series:
            if refers(cmd, i.name):
                g.edge(nnaming(name), snaming(i.name))

    def subg_table(self, g):
        g.attr('node', shape='rectangle')
        for n in self.tables:
            g.node(nnt(n.name), label=n.name)

    def subg_view(self, g):
        g.attr('edge', arrowhead='dot')
        g.attr('node', shape='trapezium')
        for n in self.views:
            g.node(nnv(n.name), label=n.name)
            self.depends(g, n.name,  nnv, n.cmd, self.tables, nnt)

    def subg_queries(self, g):
        g.attr('edge', arrowhead='dot')
        for query in queries(self.datasource):
            g.node(nnq(query.name), label=query.name)
            cmd = query.cmd
            self.depends(g, query.name, nnq, cmd, self.tables, nnt)
            self.depends(g, query.name, nnq, cmd, self.views, nnv)

    def subg_forms(self, g):
        g.attr('node', shape='rect', style='filled', fillcolor='#ffcc99')
        g.attr('edge', arrowhead='dot')
        for i in self.forms.ElementNames:
            self.handle_form(g, i, self.dbdoc)

    def handle_form(self, g, fname, doc):
        g.node(fname)
        form = openForm(doc, fname)
        for f in form.win.DrawPage.Forms:
            print(fname, f.Command)
            self.handle_inner_form(g, form,  f)

        form.obj.close()

    def handle_form_command(self, g, mform, form):
        fname = mform.name
        cmd = form.Command
        if form.CommandType == TABLE_TYPE:
            for v in self.views:
                cmd = form.Command
                if cmd == v.name:
                    g.edge(fname, nnv(cmd))
                    return
            g.edge(fname, nnt(cmd), arrowhead='box', color='red')
        else:
            if form.CommandType == QUERY_TYPE:
                g.edge(fname, nnq(cmd))

    def handle_inner_form(self, g,  mform, form):
        self.handle_form_command(g, mform, form)
        for i in form:
            print("Control name", i.Name)
            if i.getServiceName() == 'stardiv.one.form.component.ListBox':
                if 'QUERY' in str(i.ListSourceType):
                    print(i.ListSource)
                    g.edge(mform.name, nnq(i.ListSource))
            if i.getServiceName() == 'stardiv.one.form.component.Form':
                print('subform', i.Command)
                self.handle_inner_form(g, mform, i)

    def buildGraph(self):
        g = Digraph('G', filename=os.path.basename(
            self.datasource.Name) + '.gv')
        g.attr('graph', rankdir='LR')
        with g.subgraph(name='tables') as t:
            self.subg_table(t)  # t.attr(rank='same')
        with g.subgraph(name='views') as v:
            self.subg_view(v)
        with g.subgraph(name='queries') as q:
            self.subg_queries(q)
        with g.subgraph(name='forms') as f:
            self.subg_forms(f)
        return g


def buildGraph(datasource):
    dbdeps = DBDeps(datasource)
    return dbdeps.buildGraph()


def graph():
    try:
        db = XSCRIPTCONTEXT.getDocument().DataSource  # @UndefinedVariable
    except AttributeError:
        from apso_utils import msgbox
        msgbox("No database file open")
        return
    buildGraph(db)


def consoleDlg():
    ctx = XSCRIPTCONTEXT.getComponentContext()  # @UndefinedVariable
    smgr = ctx.getServiceManager()
    dp = smgr.createInstanceWithContext("com.sun.star.awt.DialogProvider", ctx)
    dlg = dp.createDialog(
        "vnd.sun.star.script:Access2Base.dlgTrace?location=application")
    dlg.execute()
    dlg.dispose()

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
#         handle_form(f)
#
#
# def reportDemo():
#     for r in reports:
#         report(r)

# if __name__ == 'main':
