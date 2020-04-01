import uno
getConstantByName = uno.pyuno.getConstantByName

import collections

Form = collections.namedtuple('Form', 'name obj win')
def openForm(doc, fname):
    obj = doc.FormDocuments.getByName(fname)
    control = doc.CurrentController
    control.connect()
    formtype = getConstantByName('com.sun.star.sdb.application.DatabaseObject.FORM')
    win = control.loadComponent(formtype, fname, False)
    win.CurrentController.Frame.ContainerWindow.setVisible(False)
    
    return Form(name=fname,
                obj=obj,
                win=win)