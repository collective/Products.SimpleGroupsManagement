from zope.component.interfaces import IObjectEvent,ObjectEvent
from zope.interface import implements

class IUserAddedToGroup(IObjectEvent):
    """An user has been added to a group
    """

class UserAddedToGroup(ObjectEvent):
    """ """
    implements(IUserAddedToGroup)

    def __init__(self, group, user_id) :
        """ """
        super(UserAddedToGroup, self).__init__({'user_id':user_id,'group':group})