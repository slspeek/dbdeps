import uno

from dbdeps import *
from dbdeps.open_helper import *
localContext = uno.getComponentContext()

# create the UnoUrlResolver
resolver = localContext.ServiceManager.createInstanceWithContext(
    "com.sun.star.bridge.UnoUrlResolver", localContext)

# connect to the running office
ctx = resolver.resolve(
    "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
smgr = ctx.ServiceManager


def datasource():
    ddctx = smgr.createInstance("com.sun.star.sdb.DatabaseContext")
    return ddctx.getByName("testdb")

def datasource2():
    ddctx = smgr.createInstance("com.sun.star.sdb.DatabaseContext")
    return ddctx.getByName("Automobile")

ds = datasource()

doc = ds.DatabaseDocument


#  d = DBDeps(ds)
