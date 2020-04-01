import uno
localContext = uno.getComponentContext()

# create the UnoUrlResolver
resolver = localContext.ServiceManager.createInstanceWithContext(
                "com.sun.star.bridge.UnoUrlResolver", localContext)

# connect to the running office
ctx = resolver.resolve("uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
smgr = ctx.ServiceManager

def datasource():
    ddctx = smgr.createInstance("com.sun.star.sdb.DatabaseContext")
    return ddctx.getByName("testdb")

ds = datasource()

doc = ds.DatabaseDocument

from dbdeps.open_helper import openForm
