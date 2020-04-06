from functools import partial
import os

from graphviz import Digraph

from dbdeps.open_helper import *
from dbdeps.sql_helper import refers
from dbdeps.table import *


# get the uno component context from the PyUNO runtime
# import uno
getConstantByName = uno.pyuno.getConstantByName
TABLE_TYPE = getConstantByName('com.sun.star.sdb.CommandType.TABLE')
QUERY_TYPE = getConstantByName('com.sun.star.sdb.CommandType.QUERY')
COMMAND_TYPE = getConstantByName('com.sun.star.sdb.CommandType.COMMAND')


def prefix(pre, name):
    return '{0}_{1}'.format(pre, name)


nnt = partial(prefix, 'table')
nnv = partial(prefix, 'view')
nnq = partial(prefix, 'query')
nnf = partial(prefix, 'form')
nnr = partial(prefix, 'report')


class DependencyCalculator(object):

    def __init__(self, tables, views, queries):
        self.tables = tables
        self.views = views
        self.queries = queries

    def execute(self, g, node_name, cmd):
        if cmd.cmdType == TABLE_TYPE:
            node_name_func = nnt
            if cmd.cmd in self.views:
                node_name_func = nnv
            else:
                # We are a real DB TABLE
                if node_name.startswith('form'):
                    g.edge(node_name, node_name_func(cmd.cmd),
                           arrowhead='box', color='red')
                    return
            g.edge(node_name, node_name_func(cmd.cmd))
        else:
            if cmd.cmdType == QUERY_TYPE:
                g.edge(node_name, nnq(cmd.cmd))
            else:
                if cmd.cmdType == COMMAND_TYPE:
                    self.depends(g, node_name, cmd.cmd, self.tables, nnt)
                    self.depends(g, node_name, cmd.cmd, self.views, nnv)
                    self.depends(g, node_name, cmd.cmd, self.queries, nnq)

    def depends(self, g,  node_name, sql, series, snaming):
        for i in series:
            if refers(sql, i):
                g.edge(node_name, snaming(i))


class DBDeps(object):

    def init_reports(self):
        rv = []
        for r in self.dbdoc.ReportDocuments.ElementNames:
            rv.append(open_report(self.dbdoc, r))
        return rv

    def __init__(self, datasource):
        self.c = datasource.getConnection('sa', '')
        self.datasource = datasource
        self.tables = tables(self.c)
        self.views = views(self.c)
        self.queries = queries(self.datasource)
        self.dbdoc = datasource.DatabaseDocument
        self.forms = self.dbdoc.FormDocuments
        self.reports = self.init_reports()
        self.calculator = DependencyCalculator(list(map(lambda x: x.name, self.tables)),
                                               list(
                                                   map(lambda x: x.name, self.views)),
                                               list(map(lambda x: x.name, self.queries)))

    def depends(self, g,  name, nnaming, cmd, series, snaming):
        for i in series:
            if refers(cmd, i.name):
                g.edge(nnaming(name), snaming(i.name))

    def subg_table(self, g):
        g.attr('node', shape='cylinder', style='filled', fillcolor="#a7c3eb")
        for n in self.tables:
            g.node(nnt(n.name), label=n.name)
            for k in n.keys:
                if k.referenced_table:
                    g.edge(nnt(n.name), nnt(k.referenced_table))

    def subg_view(self, g):
        g.attr('edge', arrowhead='dot')
        g.attr('node', shape='hexagon')
        for n in self.views:
            g.node(nnv(n.name), label=n.name)
            self.calculator.execute(g, nnv(n.name), Cmd(
                cmd=n.cmd, cmdType=COMMAND_TYPE))

    def subg_queries(self, g):
        g.attr('edge', arrowhead='dot')
        for query in queries(self.datasource):
            g.node(nnq(query.name), label=query.name)
            self.calculator.execute(g, nnq(query.name), Cmd(
                cmd=query.cmd, cmdType=COMMAND_TYPE))

    def subg_forms(self, g):
        g.attr('node', shape='rect', style='filled', fillcolor='#ffcc99')
        g.attr('edge', arrowhead='dot')
        for i in self.forms.ElementNames:
            self.handle_form(g, i, self.dbdoc)

    def handle_form(self, g, fname, doc):
        g.node(nnf(fname), label=fname)
        form = open_form(doc, fname)
        for f in form.win.DrawPage.Forms:
            print(fname, f.Command, f.CommandType)
            self.handle_inner_form(g, form,  f)

        form.obj.close()

    def handle_form_command(self, g, mform, inner_form):
        fname = mform.name
        cmd = inner_form.Command
        cmdType = inner_form.CommandType
        self.calculator.execute(g, nnf(fname), Cmd(cmd=cmd, cmdType=cmdType))

    def handle_inner_form(self, g,  mform, form):
        self.handle_form_command(g, mform, form)
        for i in form:
            print("Control name", i.Name)
            if i.getServiceName() == 'stardiv.one.form.component.ListBox':
                if 'QUERY' in str(i.ListSourceType):
                    print(i.ListSource)
                    g.edge(nnf(mform.name), nnq(i.ListSource[0]))
                if 'TABLE' in str(i.ListSourceType):
                    print(i.ListSource)
                    g.edge(nnf(mform.name), nnt(i.ListSource[0]))
                if 'SQL' in str(i.ListSourceType):
                    print(i.ListSource)
                    self.calculator.execute(g, nnf(mform.name), Cmd(
                        cmd=i.ListSource, cmdType=COMMAND_TYPE))

            if i.getServiceName() == 'stardiv.one.form.component.Form':
                print('subform', i.Command)
                self.handle_inner_form(g, mform, i)

    def subg_reports(self, g):
        g.attr('node', shape='note', style='filled', fillcolor="#c4e5ff")
        g.attr('edge', arrowhead='dot')
        for r in self.reports:
            g.node(nnr(r.name), label=r.name)
            self.calculator.execute(g, nnr(r.name), r.cmd)

    def build_graph(self):
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
        with g.subgraph(name='reports') as r:
            self.subg_reports(r)

        return g


def build_graph(datasource):
    dbdeps = DBDeps(datasource)
    return dbdeps.build_graph()

