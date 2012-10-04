from Products.CMFCore.utils import getToolByName

# Properties are defined here, because if they are defined in propertiestool.xml,
# all properties are re-set the their initial state if you reinstall product
# in the quickinstaller.

_PROPERTIES = [
    dict(name='sgm_data', type_='lines', value=()),
    dict(name='sgm_never_managed_groups', type_='lines', value=('Administrators',
                                                                'Site Administrators',
                                                                'Reviewers',
                                                                'AuthenticatedUsers'))
    ]

def import_various(context):
    if context.readDataFile('simplegroupsmanagement-various.txt') is None:
        return
    # Define portal properties
    site = context.getSite()
    ptool = getToolByName(site, 'portal_properties')
    props = getattr(ptool, 'simple_groups_management_properties',None)
    if not props:
        ptool.addPropertySheet(id='simple_groups_management_properties',title="SimpleGroupsManagement properties")
        site.plone_log("Added SimpleGroupsManagement properties protperty sheet")
        props = getattr(ptool, 'simple_groups_management_properties',None)
    for prop in _PROPERTIES:
        if not props.hasProperty(prop['name']):
            props.manage_addProperty(prop['name'], prop['value'], prop['type_'])
    
