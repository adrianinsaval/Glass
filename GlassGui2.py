# Glass module for FreeCAD
# Copyright (C) 2018 triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

"""Glass module for FreeCAD - Gui."""


import FreeCADGui as Gui
import FreeCAD
from PySide import QtGui
from PySide import QtCore

mode = 0
wid = QtGui.QWidget()
mw = Gui.getMainWindow()
mdi = mw.findChild(QtGui.QMdiArea)


def findDock():
    """Find combo view widget."""
    global dock
    dock = mw.findChild(QtGui.QDockWidget, "Tree view")


def createActions():
    """Create actions."""
    a1 = QtGui.QAction(mw)
    a1.setParent(mw)
    a1.setText("Glass toggle dock mode")
    a1.setObjectName("Glass2ToggleMode")
    a1.setShortcut(QtGui.QKeySequence("Q, 3"))
    a1.triggered.connect(setMode)
    mw.addAction(a1)
    a2 = QtGui.QAction(mw)
    a2.setParent(mw)
    a2.setText("Glass toggle dock visibility")
    a2.setObjectName("Glass2ToggleVisibility")
    a2.setShortcut(QtGui.QKeySequence("Q, 4"))
    a2.triggered.connect(setVisibility)
    mw.addAction(a2)


def applyGlass(boolean, widget):
    """Apply or remove glass."""
    try:
        if boolean:
            widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        else:
            widget.setWindowFlags(dock.windowFlags() & ~QtCore.
                                  Qt.
                                  FramelessWindowHint)
    except:
        pass
    try:
        widget.setAttribute(QtCore.Qt.WA_NoSystemBackground, boolean)
    except:
        pass
    try:
        widget.setAttribute(QtCore.Qt.WA_TranslucentBackground, boolean)
    except:
        pass
    try:
        if boolean:
            widget.setStyleSheet("background:transparent; border:none; color: white;")
        else:
            widget.setStyleSheet("")
    except:
        pass
    try:
        if boolean:
            widget.setVerticalScrollBarPolicy((QtCore.Qt.ScrollBarAlwaysOff))
        else:
            widget.setVerticalScrollBarPolicy((QtCore.Qt.ScrollBarAsNeeded))
    except:
        pass
    try:
        if boolean:
            widget.setHorizontalScrollBarPolicy((QtCore.Qt.ScrollBarAsNeeded))
        else:
            widget.setHorizontalScrollBarPolicy((QtCore.Qt.ScrollBarAsNeeded))
    except:
        pass
    try:
        widget.setDocumentMode(boolean)
    except:
        pass
    try:
        widget.tabBar().setDrawBase(False)
    except:
        pass
    try:
        if boolean:
            widget.header().hide()
        else:
            widget.header().show()
    except:
        pass


def widgetList(boolean):
    """List of child widgets."""
    children = []
    children.append(dock)

    child = True
    while child:
        child = False
        for i in children:
            if i.children():
                for c in i.children():
                    if c not in children:
                        children.append(c)
                        child = True

    for child in children:
        applyGlass(boolean, child)


def setMode():
    """Set dock or overlay widget mode."""
    global mode

    if mode == 0:
        dock.setParent(mdi)
        dock.setTitleBarWidget(wid)
        wid.hide()
        dock.show()
        widgetList(True)
        mode = 1
    else:
        dock.setParent(mw)
        dock.setTitleBarWidget(None)
        mw.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
        dock.show()
        widgetList(False)
        mode = 0

    onResize()


def setVisibility():
    """Toggle visibility."""
    dock.toggleViewAction().trigger()
    if dock.isVisible():
        mw.findChild(QtGui.QWidget,'Combo View').findChild(QtGui.QWidget, 'propertyTab').parent().parent().setSizes([0,1]) # look for the property editor parent (is a QSplitter) and apply sizes to hide treeview
    else:
        mw.findChild(QtGui.QWidget,'Combo View').findChild(QtGui.QWidget, 'propertyTab').parent().parent().setSizes([mdi.geometry().height()/2,mdi.geometry().height()/2]) # look for the property editor parent (is a QSplitter) and apply sizes to show treeview


def onResize():
    """Resize dock."""
    if mode == 1:
        x = mdi.geometry().width() - 230
        y = 160
        w = 230
        h = (mdi.geometry().height() -
             mdi.findChild(QtGui.QTabBar).geometry().height()) - 160
        dock.setGeometry(x, y, w, h)


def onStart():
    """Start the glass module."""
    if mw.property("eventLoop"):
        timer.stop()
        timer.timeout.disconnect(onStart)
        findDock()
        createActions()
        if FreeCAD.ParamGet("User parameter:BaseApp/Glass").GetBool("glassAuto",1):
            setMode() # activate Glass mode
            if dock.isVisible():
                mw.findChild(QtGui.QWidget,'Combo View').findChild(QtGui.QWidget, 'propertyTab').parent().parent().setSizes([0,1]) # look for the property editor parent (is a QSplitter) and apply sizes to hide treeview
        Gui.ActiveDocument.ActiveView.setAxisCross(True)
        timer.timeout.connect(onResize)
        timer.start(2000)


timer = QtCore.QTimer()
timer.timeout.connect(onStart)
timer.start(500)
