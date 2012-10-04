# -*- coding: utf-8 -*-

def uninstall(portal, reinstall=False):
    setup_tool = portal.portal_setup
    if not reinstall:
        setup_tool.runAllImportStepsFromProfile('profile-Products.SimpleGroupsManagement:uninstall')
