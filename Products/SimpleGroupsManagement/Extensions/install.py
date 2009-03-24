# -*- coding: utf-8 -*-

__author__ = """RedTurtle Technology"""
__docformat__ = 'plaintext'

from Products.Archetypes.public import listTypes
import string
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import getFSVersionTuple
from StringIO import StringIO

from Products.SimpleGroupsManagement import config

def install(self, reinstall=False):
    out = StringIO()

    configPortalSetup(self, out)

    print >> out, "Successfully installed"
    return out.getvalue()

def configPortalSetup(self, out):
    """Install GS profile"""
    portal_setup=getToolByName(self, "portal_setup")

    if getFSVersionTuple()[:3]>=(3,0,0):
        portal_setup.runAllImportStepsFromProfile(
                "profile-Products.%s:default" % config.PROJECTNAME,
                purge_old=False)
    else:
        plone_base_profileid = "profile-CMFPlone:plone"
        portal_setup.setImportContext(plone_base_profileid)
        portal_setup.setImportContext("profile-Products.%s:default" % config.PROJECTNAME)
        portal_setup.runAllImportSteps(purge_old=False)
        portal_setup.setImportContext(plone_base_profileid)

    print >> out, "Installed GS profile"
