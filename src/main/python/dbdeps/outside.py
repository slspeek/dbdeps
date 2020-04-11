import uno
import time

localContext = uno.getComponentContext()

# create the UnoUrlResolver
resolver = localContext.ServiceManager.createInstanceWithContext(
    "com.sun.star.bridge.UnoUrlResolver", localContext)

ctx = 'Error'
while(True):
    try:
        # connect to the running office
        ctx = resolver.resolve(
        "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
        break
    except:
        time.sleep(0.1)
        
  
smgr = ctx.ServiceManager


def datasource():
    ddctx = smgr.createInstance("com.sun.star.sdb.DatabaseContext")
    return ddctx.getByName("testdb")

def datasource2():
    ddctx = smgr.createInstance("com.sun.star.sdb.DatabaseContext")
    return ddctx.getByName("Automobile")

