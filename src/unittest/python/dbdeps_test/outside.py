import time
import logging

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)
def wait_for_connection():
    import uno
#         time.sleep(3) # needed if no --headless
    localContext = uno.getComponentContext()

    # create the UnoUrlResolver
    resolver = localContext.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", localContext)

    ctx = 'Error'
    i = 0
    while(i < 50):
        try:
            # connect to the running office
            ctx = resolver.resolve(
                "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext")
            break
        except:
            i += 1
            logger.debug('waiting on uno connection')
            time.sleep(0.1)

    return ctx.ServiceManager

smgr = wait_for_connection()

def desktop():
    return smgr.createInstance("com.sun.star.frame.Desktop")

def datasource():
    ddctx = smgr.createInstance("com.sun.star.sdb.DatabaseContext")
    return ddctx.getByName("testdb")

