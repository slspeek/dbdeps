import collections
import uno


getConstantByName = uno.pyuno.getConstantByName
FORM_TYPE = getConstantByName(
    'com.sun.star.sdb.application.DatabaseObject.FORM')
REPORT_TYPE = getConstantByName(
    'com.sun.star.sdb.application.DatabaseObject.REPORT')


Form = collections.namedtuple('Form', 'name obj win')
Report = collections.namedtuple('Report', 'name cmd')
Cmd = collections.namedtuple('Cmd', 'cmd cmdType')


def open_form(doc, fname):
    obj = doc.FormDocuments.getByName(fname)
    control = doc.CurrentController
    control.connect()
    win = control.loadComponent(FORM_TYPE, fname, False)
    win.CurrentController.Frame.ContainerWindow.setVisible(False)

    return Form(name=fname,
                obj=obj,
                win=win)


def open_report(doc, rname):
    obj = doc.ReportDocuments.getByName(rname)
    control = doc.CurrentController
    control.connect()
    win = control.loadComponent(REPORT_TYPE, rname, True)
    win.CurrentController.Frame.ContainerWindow.setVisible(False)
    cmd = win.Command
    cmdType = win.CommandType
    cmdS = Cmd(cmd=cmd, cmdType=cmdType)
    obj.close()

    return Report(name=rname,
                  cmd=cmdS)
