from zope.component.interfaces import IObjectEvent, ObjectEvent
from zope.interface import implementer


class IUserAddedToGroup(IObjectEvent):
    """Marker interface for user that is added to a group"""


class IUserRemovedFromGroup(IObjectEvent):
    """AMarker interface for user that is removed from a group"""


@implementer(IUserAddedToGroup)
class UserAddedToGroup(ObjectEvent):
    """Event fired when a user is added to a group"""

    def __init__(self, group, user_id):
        super(UserAddedToGroup, self).__init__({"user_id": user_id, "group": group})


@implementer(IUserRemovedFromGroup)
class UserRemovedFromGroup(ObjectEvent):
    """Event fired when a user is removed from a group"""

    def __init__(self, group, user_id):
        super(UserRemovedFromGroup, self).__init__({"user_id": user_id, "group": group})
