# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.PlonePAS.permissions import ManageGroups
from plone import api
from ..interfaces import ISimpleGroupManagementSettings


class CheckSimpleGroupsManagement(BrowserView):
    """View for check if an user can manage some groups"""

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.acl_users = getToolByName(context, "acl_users")
        self.sgm_data = api.portal.get_registry_record(
            "sgm_data", interface=ISimpleGroupManagementSettings
        )

    def __call__(self):
        """Check the SGM settings and find if the user can manage some groups
        """
        context = self.context
        member = getToolByName(context, "portal_membership").getAuthenticatedMember()
        if member.has_permission(ManageGroups, context):
            return True

        my_groups = member.getGroups()
        for line in self.sgm_data:
            line = line.strip()
            if line.find("|") == -1:
                continue
            id, group_id = line.split("|")
            if id == member.getId() or id in my_groups:
                group = self.acl_users.getGroup(group_id)
                if group:
                    return True
        return False
