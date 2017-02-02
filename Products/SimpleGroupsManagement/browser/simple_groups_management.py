# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PlonePAS.permissions import ManageGroups
from Products.SimpleGroupsManagement import messageFactory as _
from Products.SimpleGroupsManagement.group_event import UserAddedToGroup
from Products.SimpleGroupsManagement.group_event import UserRemovedFromGroup
from itertools import chain
from plone import api
from plone.api.exc import InvalidParameterError
from zope.component import getMultiAdapter
from zope.event import notify
from ..interfaces import ISimpleGroupManagementSettings


class SimpleGroupsManagement(BrowserView):
    """Main view for manage groups in the Plone portal"""

    main_template = ViewPageTemplateFile("simple_groups_management.pt")
    manage_group_template = ViewPageTemplateFile("manage_group_template.pt")

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        portal_properties = getToolByName(context, 'portal_properties')
        self.acl_users = getToolByName(context, 'acl_users')
        self.sgm_data = api.portal.get_registry_record(
            'sgm_data', interface=ISimpleGroupManagementSettings
        )
        self.never_used_groups = api.portal.get_registry_record(
            'sgm_never_managed_groups', interface=ISimpleGroupManagementSettings
        )

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

    @property
    def many_users(self):
        try:
            many_users = api.portal.get_registry_record('plone.many_users')
        except InvalidParameterError:
            # Plone 4 probably
            many_users = getToolByName(
                self.context, 'portal_properties'
            ).site_properties
        return many_users

    def check_groups_management_permission(self):
        """
        Check the simple_groups_management_properties property sheets and find
        if the user can manage some groups
        """
        context = self.context
        member = getToolByName(
            context, 'portal_membership'
        ).getAuthenticatedMember()
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
        """
        Obtain a list of all groups that can be managed by the current user
        """
        context = self.context
        member = getToolByName(
            context, 'portal_membership').getAuthenticatedMember()
        manageable_groups = []
        if member.has_permission(ManageGroups, context):
            manageable_groups = self.acl_users.searchGroups()
        else:
            group_objects = self._getSimpleGroupsManagementConfiguration()
            ids_list = [x.getId() for x in group_objects]
            if ids_list == []:
                return ids_list
            manageable_groups = self.acl_users.searchGroups(
                exact_match=True,
                id=ids_list
            )
        return [x for x in manageable_groups
                if x.get('id') not in self.never_used_groups]

    def manageableGroupIds(self):
        """
        return a list of ids of manageable groups
        """
        manageable_groups = self.manageable_groups()
        return [x.get('id') for x in manageable_groups
                if x.get('id') not in self.never_used_groups]

    def can_addusers(self):
        """Check if the current member can add news users"""
        context = self.context
        member = getToolByName(
            context, 'portal_membership').getAuthenticatedMember()
        return member.has_permission(permissions.AddPortalMember, context)

    def load_portalmembers(self, ignore=[]):
        """Return all members of the portal"""
        mtool = getToolByName(self.context, 'portal_membership')
        searchString = self.request.form.get('searchstring')
        searchView = getMultiAdapter(
            (aq_inner(self.context), self.request), name='pas_search')
        if self.request.form.get('form.button.FindAll'):
            userResults = searchView.searchUsers(sort_by='userid')
        elif self.request.form.get('form.button.Search') and searchString:
            userResults = searchView.merge(
                chain(
                    *[searchView.searchUsers(
                        **{field: searchString}
                    ) for field in ['login', 'fullname', 'email']]
                ), 'userid'
            )
        else:
            return []
        userResults = [mtool.getMemberById(u['id']) for u in userResults
                       if u['id'] not in ignore]
        userResults.sort(key=lambda x: x is not None and x.getProperty(
            'fullname') is not None and normalizeString(
                x.getProperty('fullname')
            ) or '')
        return userResults

    def _getSimpleGroupsManagementConfiguration(self):
        """
        Check the SGM settings and find which groups the current user can manage
        Every line of the simple_groups_management_properties.sgm_data can be:
        mygroup_id|group_id
        ...or...
        myuser_id|group_id
        """
        context = self.context
        manageable_groups = []
        member = getToolByName(
            context, 'portal_membership').getAuthenticatedMember()
        my_groups = member.getGroups()
        for line in self.sgm_data:
            line = line.strip()
            if line.find("|") == -1:
                continue
            id, group_id = line.split("|")
            if id == member.getId() or id in my_groups:
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
            notify(UserRemovedFromGroup(group, user_id))
        self.request.response.redirect(
            self.context.absolute_url() +
            '/@@simple_groups_management?group_id=%s&deleted=1' % group_id)

    def add(self):
        """Add users from the group"""
        group_id = self.request.get("group_id")
        if group_id not in self.manageableGroupIds():
            raise Unauthorized()
        user_ids = self.request.get("user_id")
        group = self.acl_users.getGroup(group_id)
        for user_id in user_ids:
            group.addMember(user_id)
            notify(UserAddedToGroup(group, user_id))
        self.request.response.redirect(
            self.context.absolute_url() +
            '/@@simple_groups_management?group_id=%s&added=1' % group_id)
