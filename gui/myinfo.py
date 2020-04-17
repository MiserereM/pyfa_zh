import wx
import gui.mainFrame
from gui.auxFrame import AuxiliaryFrame
class myInfoFrame(AuxiliaryFrame):
    # def __init__(self, parent, id):
    #     wx.Frame.__init__(self, parent, id, u'汉化说明',style=wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_NO_TASKBAR)
    #     psize = parent.GetSize()
    #     ppos = parent.GetPosition()
    #     self.SetPosition(ppos)
    #     self.SetSize((600, 300))
    #     # 创建面板
    #     panel = wx.Panel(self)
    #
    #     # 在Panel上添加Button
    #     # text = "本程序由Miserere Mei Deus个人无责任汉化\nSpecialized pig-farm.（专业养猪场）诚挚招新\n详情加群咨询562634438"
    #     # text = "本程序由Miserere Mei Deus个人无责任汉化\n\n\nSpecialized pig-farm.（专业养猪场）诚挚招新\n我们不能提供：\n1.入团福利  2.新人一对一教学  3.出勤奖励  4.旗舰保护伞\n我们能提供：\n1.进出洞的快感  2.叔叔带你看大鱼的成就感\n3.并不值钱的姐妹会任务点  4.被敌对包围的gay伦特五级任务点  5.绝对不会红的天蛇死亡\n详情加群咨询"
    #     text = "本程序由Miserere Mei Deus个人无责任汉化\n\nSpecialized pig-farm.（专业养猪场）诚挚招新\n我们是低安狂魔、孤儿猎手、捕鱼达人，是一个集低安和高洞于一体的联盟\n目前建制为三神裔战巡及重突，每周有固定活动，现开放招募\n详情加群咨询562634438"
    #     wx.StaticText(panel, -1, text, (10, 10))
    def __init__(
            self
    ):
        super().__init__(
            parent=gui.mainFrame.MainFrame.getInstance(),
            id=wx.ID_ANY,
            title="汉化说明",
            resizeable=True
        )
        self.style = wx.FRAME_FLOAT_ON_PARENT|wx.FRAME_NO_TASKBAR
        parent = gui.mainFrame.MainFrame.getInstance()
        ppos = parent.GetPosition()
        size = parent.GetSize()
        self.SetPosition((ppos.x+(size.x/2)-300,ppos.y+(size.y/2)-150))
        self.SetSize((600, 300))
        panel = wx.Panel(self)
        text = "本程序由Miserere Mei Deus个人无责任汉化\n" \
               "如有问题欢迎游戏内邮件联系\n\n" \
               "Specialized pig-farm.（专业养猪场）诚挚招新\n"\
               "我们是低安狂魔、孤儿猎手、捕鱼达人，是一个集低安和高洞于一体的联盟\n" \
               "目前建制为三神裔战巡及重突，每周有固定活动，现开放招募\n" \
               "我们能提供\n" \
               "1.进出洞的快感\n" \
               "2.叔叔带你看大鱼的成就感\n" \
               "3.并不值钱的姐妹会任务点\n" \
               "4.被敌对包围的gay伦特五级任务点\n" \
               "5.绝对不会红的天蛇死亡\n" \
               "详情加群咨询562634438"
        wx.StaticText(panel, -1, text, (10, 10))
