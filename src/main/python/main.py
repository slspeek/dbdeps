from dbdeps import build_graph

def graph():
    try:
        db = XSCRIPTCONTEXT.getDocument().DataSource  # @UndefinedVariable
    except AttributeError:
        pass
#         from apso_utils import msgbox
#         msgbox("No database file open")
#         return
    g = build_graph(db)
    g.view()

g_exportedScripts = (graph,)
