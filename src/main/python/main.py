from dbdeps import build_graph

def graph():
    try:
        db = XSCRIPTCONTEXT.getDocument().DataSource  # @UndefinedVariable
    except AttributeError:
        return

    g = build_graph(db)
    g.view()

g_exportedScripts = (graph,)
