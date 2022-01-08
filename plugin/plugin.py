##
## Blackout blind by mrvica, puts a black bar on top of the screen to hide VBI lines, shamelessly stolen from PermanentClock plugin
##
from .__init__ import _
from Components.ActionMap import ActionMap
from Components.config import config, ConfigInteger, ConfigSubsection, ConfigYesNo
from Components.MenuList import MenuList
from enigma import getDesktop
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.Sources.StaticText import StaticText

config.plugins.Blind = ConfigSubsection()
config.plugins.Blind.enabled = ConfigYesNo(default=False)

try:
	screenWidth = getDesktop(0).size().width()
except:
	screenWidth = 720

SKIN = '<screen position="0,0" size="%d,3" zPosition="1" title="Blind" flags="wfNoBorder">\
	    <eLabel name="blackbar" position="0,0" size="%d,3" zPosition="2" backgroundColor="#000000" foregroundColor="#000000"/>\
	</screen>' % (screenWidth, screenWidth)


class BlindScreen(Screen):

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skin = SKIN


class Blind:

    def __init__(self):
        self.dialog = None
        return

    def gotSession(self, session):
        self.dialog = session.instantiateDialog(BlindScreen)
        self.showHide()

    def changeVisibility(self):
        if config.plugins.Blind.enabled.value:
            config.plugins.Blind.enabled.value = False
        else:
            config.plugins.Blind.enabled.value = True
        config.plugins.Blind.enabled.save()
        self.showHide()

    def showHide(self):
        if config.plugins.Blind.enabled.value:
            self.dialog.show()
        else:
            self.dialog.hide()


pBlind = Blind()


class BlindMenu(Screen):
    if screenWidth >= 1920:
        skin = '<screen position="center,center" size="1030,68" title="Blackout Blind">\
            <widget name="list" font="Regular;30" itemHeight="36" position="15,15" size="1000,36" />\
	</screen>'
    else:
        skin = '<screen position="center,center" size="420,46" title="Blackout Blind">\
            <widget name="list" position="10,10" size="400,36" />\
        </screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self['list'] = MenuList([])
        self['actions'] = ActionMap(['OkCancelActions'], {'ok': self.okClicked,
         'cancel': self.close}, -1)
        self.onLayoutFinish.append(self.showMenu)

    def showMenu(self):
        list = []
        if config.plugins.Blind.enabled.value:
            list.append(_('now ON, press OK to deactivate it or Exit'))
        else:
            list.append(_('now OFF, press OK to activate it or Exit'))
        self['list'].setList(list)

    def okClicked(self):
        sel = self['list'].getCurrent()
        if pBlind.dialog is None:
            pBlind.gotSession(self.session)
        if sel == _('now ON, press OK to deactivate it or Exit') or sel == _('now OFF, press OK to activate it or Exit'):
            pBlind.changeVisibility()
            self.showMenu()
        else:
            pBlind.dialog.hide()
        return


def sessionstart(reason, **kwargs):
    if reason == 0:
        pBlind.gotSession(kwargs['session'])


def startConfig(session, **kwargs):
    session.open(BlindMenu)


def main(session, **kwargs):
    session.open(BlindMenu)


def Plugins(**kwargs):
    return [PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionstart), PluginDescriptor(name=_('Blackout Blind'), description=_('blacks out two lines on top of the screen'), where=PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)]
