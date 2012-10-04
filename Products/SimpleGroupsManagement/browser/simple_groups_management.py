# -*- coding: utf-8 -*-

from zope.event import notify

from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import permissions

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

try:
    from Products.GroupUserFolder.GroupsToolPermissions import ManageGroups
except ImportError:
    from Products.PlonePAS.permissions import ManageGroups

from Products.SimpleGroupsManagement import messageFactory as _
from Products.SimpleGroupsManagement.group_event import UserAddedToGroup, UserRemovedFromGroup

class SimpleGroupsManagement(BrowserView):
    """Main view for manage groups od the Plone portal"""

    main_template = ViewPageTemplateFile("simple_groups_management.pt")
    manage_group_template = ViewPageTemplateFile("manage_group_template.pt")

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        portal_properties = getToolByName(context, 'portal_properties')
        self.acl_users = getToolByName(context, 'acl_users')
        self.sgm_data = portal_properties['simple_groups_management_properties'].sgm_data
        self.never_used_groups = portal_properties['simple_groups_management_properties'].sgm_never_managed_groups
        
    def __call__(self):
        request = self.request
        plone_utils = getToolByName(self.context, 'plone_utils')
        if request.get('deleted'):
            plone_utils.addPortalMessage(_('Member(s) removed'))
        elif request.get('added'):
            plone_utils.addPortalMessage(_(u'Member(s) added'))
        if self.request.get("group_id"):
            return self.manage_group_template()
        return self.main_template()

    def check_groups_management_permission(self):
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

    def load_group(self, group_id=None):
        """Load a group taking using its id"""
        if not group_id:
            group_id = self.request.get("group_id")
        if group_id:
            if group_id not in self.manageableGroupIds():
                raise Unauthorized()
            return self.acl_users.getGroupById(group_id)
        return None

    def load_group_members(self, group):
        """Load member from a group"""
        if group:
            return group.getGroupMembers()
        return []
        
    def manageable_groups(self):
        """Obtain a list of all groups that can be managed by the current user"""
        context = self.context
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        manageable_groups=[]
        if member.has_permission(ManageGroups, context):
            manageable_groups = self.acl_users.searchGroups()
#            return [x.get('id') for x in manageable_groups if x.get('id') not in self.never_used_groups]
        else:
            group_objects = self._getSimpleGroupsManagementConfiguration()
            ids_list= [x.getId() for x in group_objects]
            manageable_groups = self.acl_users.searchGroups(id=ids_list)
        return [x for x in manageable_groups if x.get('id') not in self.never_used_groups]
    
    def manageableGroupIds(self):
        """
        return a list of ids of manageable groups
        """
        manageable_groups=self.manageable_groups()
        return [x.get('id') for x in manageable_groups if x.get('id') not in self.never_used_groups]

    def can_addusers(self):
        """Check if the current member can add news users"""
        context = self.context
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        return member.has_permission(permissions.AddPortalMember, context)

    def load_portalmembers(self):
        """Return all members of the portal"""
        pas_search=self.context.restrictedTraverse('@@pas_search')
        list_users=[]
        if self.request.form.get('form.button.FindAll'):
            users=pas_search.searchUsers(sort_by='userid')
        elif self.request.form.get('form.button.Search') and self.request.form.get('searchstring'):
            users=pas_search.searchUsers(sort_by='userid',
                                         fullname=self.request.form.get('searchstring'),
                                         id=self.request.form.get('searchstring'),
                                         )
        else:
            return []
        for user in users:
            user_obj=self.acl_users.getUser(user.get('id',''))
            if user_obj:
                list_users.append(user)
        return list_users
    
    def _getSimpleGroupsManagementConfiguration(self):
        """Check the simple_groups_management_properties property sheets and find which groups
        the current users can manage.
        Every line of the simple_groups_management_properties.sgm_data can be:
        mygroup_id|group_id
        ...or...
        myuser_id|group_id
        """
        context = self.context
        manageable_groups = []
        member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
        my_groups = member.getGroups()
        for line in self.sgm_data:
            line = line.strip()
            if line.find("|")==-1:
                continue
            id, group_id = line.split("|")
            if id==member.getId() or id in my_groups:
                group = self.acl_users.getGroup(group_id)
                if group:
                    manageable_groups.append(group)
        return manageable_groups

    def delete(self):
        """Delete users from the group"""
        group_id = self.request.get("group_id")
        if group_id not in self.manageableGroupIds():
            raise Unauthorized()
        user_ids = self.request.get("user_id")
        group = self.acl_users.getGroup(group_id)
        for user_id in user_ids:
            group.removeMember(user_id)
            notify(UserRemovedFromGroup(group,user_id))
        self.request.response.redirect(self.context.absolute_url()+'/@@simple_groups_management?group_id=%s&deleted=1' % group_id)

    def add(self):
        """Add users from the group"""
        group_id = self.request.get("group_id")
        if group_id not in self.manageableGroupIds():
            raise Unauthorized()
        user_ids = self.request.get("user_id")
        group = self.acl_users.getGroup(group_id)
        for user_id in user_ids:
            group.addMember(user_id)
            notify(UserAddedToGroup(group,user_id))        
        self.request.response.redirect(self.context.absolute_url()+'/@@simple_groups_management?group_id=%s&added=1' % group_id)


