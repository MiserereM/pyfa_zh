# =============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

# noinspection PyPackageRequirements
import wx

import config
import graphs
from service.character import Character
from service.fit import Fit
import gui.globalEvents as GE
from gui.bitmap_loader import BitmapLoader

from logbook import Logger

pyfalog = Logger(__name__)


class MainMenuBar(wx.MenuBar):
    def __init__(self, mainFrame):
        pyfalog.debug("Initialize MainMenuBar")
        self.characterEditorId = wx.NewId()
        self.damagePatternEditorId = wx.NewId()
        self.targetProfileEditorId = wx.NewId()
        self.implantSetEditorId = wx.NewId()
        self.graphFrameId = wx.NewId()
        self.backupFitsId = wx.NewId()
        self.exportSkillsNeededId = wx.NewId()
        self.importCharacterId = wx.NewId()
        self.exportHtmlId = wx.NewId()
        self.wikiId = wx.NewId()
        self.forumId = wx.NewId()
        self.aboutCnId = wx.NewId()
        self.saveCharId = wx.NewId()
        self.saveCharAsId = wx.NewId()
        self.revertCharId = wx.NewId()
        self.eveFittingsId = wx.NewId()
        self.exportToEveId = wx.NewId()
        self.ssoLoginId = wx.NewId()
        self.attrEditorId = wx.NewId()
        self.toggleOverridesId = wx.NewId()
        self.toggleIgnoreRestrictionID = wx.NewId()
        self.devToolsId = wx.NewId()
        self.optimizeFitPrice = wx.NewId()

        self.mainFrame = mainFrame
        wx.MenuBar.__init__(self)

        # File menu
        fileMenu = wx.Menu()
        self.Append(fileMenu, "&文件")

        fileMenu.Append(self.mainFrame.addPageId, "&新页面\tCTRL+T", "Open a new fitting tab")
        fileMenu.Append(self.mainFrame.closePageId, "&关闭当前页面\tCTRL+W", "Close the current fit")
        fileMenu.Append(self.mainFrame.closeAllPagesId, "&关闭所有页面\tCTRL+ALT+W", "Close all open fits")

        fileMenu.AppendSeparator()
        fileMenu.Append(self.backupFitsId, "&备份所有配置", "Backup all fittings to a XML file")
        fileMenu.Append(self.exportHtmlId, "导出所有配置到 &HTML", "Export fits to HTML file (set in Preferences)")

        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_EXIT)

        # Fit menu
        fitMenu = wx.Menu()
        self.Append(fitMenu, "&装配")

        fitMenu.Append(wx.ID_UNDO)
        fitMenu.Append(wx.ID_REDO)

        fitMenu.AppendSeparator()
        fitMenu.Append(wx.ID_COPY, "&复制配置到剪切板\tCTRL+C", "Export a fit to the clipboard")
        fitMenu.Append(wx.ID_PASTE, "&从剪切板粘贴配置\tCTRL+V", "Import a fit from the clipboard")

        fitMenu.AppendSeparator()
        fitMenu.Append(wx.ID_OPEN, "&导入配置\tCTRL+O", "Import fittings into pyfa")
        fitMenu.Append(wx.ID_SAVEAS, "&导出配置\tCTRL+S", "Export fitting to another format")

        fitMenu.AppendSeparator()
        fitMenu.Append(self.optimizeFitPrice, "&估价\tCTRL+D")
        graphFrameItem = wx.MenuItem(fitMenu, self.graphFrameId, "&图表\tCTRL+G")
        graphFrameItem.SetBitmap(BitmapLoader.getBitmap("graphs_small", "gui"))
        fitMenu.Append(graphFrameItem)
        if not graphs.graphFrame_enabled:
            self.Enable(self.graphFrameId, False)
        self.ignoreRestrictionItem = fitMenu.Append(self.toggleIgnoreRestrictionID, "Disable Fitting Re&strictions")

        fitMenu.AppendSeparator()
        fitMenu.Append(self.eveFittingsId, "&打开游戏内配置\tCTRL+B")
        fitMenu.Append(self.exportToEveId, "&配置导入到游戏\tCTRL+E")
        self.Enable(self.eveFittingsId, True)
        self.Enable(self.exportToEveId, True)

        # Character menu
        characterMenu = wx.Menu()
        self.Append(characterMenu, "&角色")

        characterMenu.Append(self.saveCharId, "&保存角色")
        characterMenu.Append(self.saveCharAsId, "&保存角色至")
        characterMenu.Append(self.revertCharId, "&重置角色")

        characterMenu.AppendSeparator()
        characterMenu.Append(self.importCharacterId, "&导入角色文件", "Import characters into pyfa from file")
        characterMenu.Append(self.exportSkillsNeededId, "&导出技能需求列表", "Export skills needed for this fitting")

        characterMenu.AppendSeparator()
        characterMenu.Append(self.ssoLoginId, "&管理ESI角色")

        # Global Menu
        globalMenu = wx.Menu()

        if not self.mainFrame.disableOverrideEditor:
            attrItem = wx.MenuItem(globalMenu, self.attrEditorId, "Attribute &Overrides")
            attrItem.SetBitmap(BitmapLoader.getBitmap("fit_rename_small", "gui"))
            globalMenu.Append(attrItem)
            globalMenu.Append(self.toggleOverridesId, "&Turn Overrides On")
            globalMenu.AppendSeparator()


        self.Append(globalMenu, "&通用")
        preferencesShortCut = "CTRL+," if 'wxMac' in wx.PlatformInfo else "CTRL+P"
        preferencesItem = wx.MenuItem(globalMenu, wx.ID_PREFERENCES, "&Preferences\t" + preferencesShortCut)
        preferencesItem.SetBitmap(BitmapLoader.getBitmap("preferences_small", "gui"))
        globalMenu.Append(preferencesItem)

        # Editors menu
        editorsMenu = wx.Menu()
        self.Append(editorsMenu, "&编辑")
        charEditItem = wx.MenuItem(editorsMenu, self.characterEditorId, "&编辑角色\tCTRL+K")
        charEditItem.SetBitmap(BitmapLoader.getBitmap("character_small", "gui"))
        editorsMenu.Append(charEditItem)
        implantSetEditItem = wx.MenuItem(editorsMenu, self.implantSetEditorId, "&编辑脑插\tCTRL+I")
        implantSetEditItem.SetBitmap(BitmapLoader.getBitmap("hardwire_small", "gui"))
        editorsMenu.Append(implantSetEditItem)
        damagePatternEditItem = wx.MenuItem(editorsMenu, self.damagePatternEditorId, "&编辑伤害属性")
        damagePatternEditItem.SetBitmap(BitmapLoader.getBitmap("damagePattern_small", "gui"))
        editorsMenu.Append(damagePatternEditItem)
        targetProfileEditItem = wx.MenuItem(editorsMenu, self.targetProfileEditorId, "&目标编辑")
        targetProfileEditItem.SetBitmap(BitmapLoader.getBitmap("explosive_small", "gui"))
        editorsMenu.Append(targetProfileEditItem)

        # Help menu
        helpMenu = wx.Menu()
        self.Append(helpMenu, "&帮助")
        helpMenu.Append(self.wikiId, "&Wiki", "Go to wiki on GitHub")
        helpMenu.Append(self.forumId, "&Forums", "Go to EVE Online Forum thread")
        helpMenu.AppendSeparator()
        helpMenu.Append(wx.ID_ABOUT)

        aboutCnMenu = wx.Menu()
        self.Append(aboutCnMenu, "&汉化说明")
        aboutItem = wx.MenuItem(aboutCnMenu, self.aboutCnId, "&汉化说明")
        aboutCnMenu.Append(aboutItem)
        if config.debug:
            helpMenu.Append(self.mainFrame.widgetInspectMenuID, "Open Wid&gets Inspect tool", "Open Widgets Inspect tool")
            helpMenu.Append(self.devToolsId, "Open &Dev Tools", "Dev Tools")

        self.mainFrame.Bind(GE.FIT_CHANGED, self.fitChanged)
        self.mainFrame.Bind(GE.FIT_RENAMED, self.fitRenamed)

    def fitChanged(self, event):
        event.Skip()
        activeFitID = self.mainFrame.getActiveFit()
        if activeFitID is not None and activeFitID not in event.fitIDs:
            return
        enable = activeFitID is not None
        self.Enable(wx.ID_SAVEAS, enable)
        self.Enable(wx.ID_COPY, enable)
        self.Enable(self.exportSkillsNeededId, enable)

        self.refreshUndo()

        sChar = Character.getInstance()
        charID = self.mainFrame.charSelection.getActiveCharacter()
        char = sChar.getCharacter(charID)

        # enable/disable character saving stuff
        self.Enable(self.saveCharId, not char.ro and char.isDirty)
        self.Enable(self.saveCharAsId, char.isDirty)
        self.Enable(self.revertCharId, char.isDirty)

        self.Enable(self.toggleIgnoreRestrictionID, enable)

        if activeFitID:
            sFit = Fit.getInstance()
            fit = sFit.getFit(activeFitID)

            if fit.ignoreRestrictions:
                self.ignoreRestrictionItem.SetItemLabel("Enable Fitting Re&strictions")
            else:
                self.ignoreRestrictionItem.SetItemLabel("Disable Fitting Re&strictions")

    def fitRenamed(self, event):
        self.refreshUndo()
        event.Skip()

    def refreshUndo(self):
        command = self.mainFrame.command
        self.Enable(wx.ID_UNDO, False)
        self.Enable(wx.ID_REDO, False)
        if command.CanUndo():
            self.Enable(wx.ID_UNDO, True)
        if command.CanRedo():
            self.Enable(wx.ID_REDO, True)
