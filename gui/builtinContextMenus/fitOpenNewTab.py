# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from graphs.wrapper import BaseWrapper
from gui.builtinShipBrowser.events import FitSelected
from gui.contextMenu import ContextMenuSingle


class OpenFitInNewTab(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in ("projectedFit", "commandFit", "graphFitListMisc", "graphTgtListMisc"):
            return False

        if mainItem is None:
            return False

        if isinstance(mainItem, BaseWrapper):
            if not mainItem.isFit:
                return False
            mainItem = mainItem.item

        currentFitID = self.mainFrame.getActiveFit()
        selectedFitID = mainItem.ID
        if currentFitID == selectedFitID:
            return False
        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return "在新装配页面打开"

    def activate(self, callingWindow, fullContext, mainItem, i):
        if isinstance(mainItem, BaseWrapper):
            mainItem = mainItem.item
        wx.PostEvent(self.mainFrame, FitSelected(fitID=mainItem.ID, startup=2))


OpenFitInNewTab.register()
