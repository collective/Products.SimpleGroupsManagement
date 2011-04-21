# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
try:
    from Products.GroupUserFolder.GroupsToolPermissions import ManageGroups
except ImportError:
    from Products.PlonePAS.permissions import ManageGroups

class CheckSimpleGroupsManagement(BrowserView):
    """View for check if an user can manage some groups"""

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        portal_properties = getToolByName(context, 'portal_properties')
        self.acl_users = getToolByName(context, 'acl_users')
        self.sgm_data = portal_properties['simple_groups_management_properties'].sgm_data
        self.never_used_groups = portal_properties['simple_groups_management_properties'].sgm_never_managed_groups
        
    def __call__(self):
        """Check the simple_groups_management_properties property sheets and find if the user can manage some groups
        """
        context = self.context
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        if member.has_permission(ManageGroups, context):
            return True

        my_groups = member.getGroups()
        for line in self.sgm_data:
            line = line.strip()
            if line.find("|")==-1:
                continue
            id, group_id = line.split("|")
            if id==member.getId() or id in my_groups:
                group = self.acl_users.getGroup(group_id)
                if group:
                    return True
        return False
