# -*- coding: utf-8 -*-
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ as os_environ
import gettext


def localeInit():
	lang = language.getLanguage()[:2] # getLanguage returns e.g. "fi_FI" for "language_country"
	os_environ["LANGUAGE"] = lang # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs it!
	gettext.bindtextdomain("BlackoutBlind", resolveFilename(SCOPE_PLUGINS, "Extensions/BlackoutBlind/locale"))


def _(txt):
	t = gettext.dgettext("BlackoutBlind", txt)
	if t == txt:
		print("[BlackoutBlind] fallback to default translation for %s" % txt)
		t = gettext.gettext(txt)
	return t


localeInit()
language.addCallback(localeInit)
