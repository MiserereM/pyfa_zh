import gui.fitCommands as cmd
import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from gui.fitCommands.helpers import droneStackLimit
from service.fit import Fit


class DroneAddStack(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext not in ('marketItemGroup', 'marketItemMisc'):
            return False

        if self.mainFrame.getActiveFit() is None:
            return False

        if mainItem is None:
            return False

        if mainItem.category.name != 'Drone':
            return False

        fitID = self.mainFrame.getActiveFit()
        fit = Fit.getInstance().getFit(fitID)
        amount = droneStackLimit(fit, mainItem)
        if amount < 1:
            return False

        self.amount = amount
        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return '添加 {} 到无人机挂仓{}'.format(
            itmContext, '' if self.amount == 1 else ' (x{})'.format(self.amount))

    def activate(self, callingWindow, fullContext, mainItem, i):
        command = cmd.GuiAddLocalDroneCommand(
            fitID=self.mainFrame.getActiveFit(),
            itemID=int(mainItem.ID),
            amount=self.amount)
        if self.mainFrame.command.Submit(command):
            self.mainFrame.additionsPane.select('Drones', focus=False)


DroneAddStack.register()
