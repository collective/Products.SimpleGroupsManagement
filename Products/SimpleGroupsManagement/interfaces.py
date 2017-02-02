# -*- coding: utf-8 -*-

from zope import schema
from zope.interface import Interface
from . import messageFactory as _


class ISimpleGroupManagementLayer(Interface):
    """Marker interface for Simple Groups Management product layer
    """


class ISimpleGroupManagementSettings(Interface):
    """Settings used in the control panel for simple group management
    """

    sgm_data = schema.Tuple(
        title=_(u"Groups management proxy"),
        description=_(
            "help_sgm_data",
            default=u"Configure which users or groups can manage which groups.\n"
                    u"Fill the field below by providing a set of \"user_foo_id|group_bar_id\""
                    u" (or \"group_foo_id|group_bar_id\"), one per line.\n"
                    u"That means: the user/group on the left of the \"|\" can handle"
                    u" group on the right."
        ),
        required=False,
        value_type=schema.TextLine(),
        default=(),
        missing_value=(),
    )

    sgm_never_managed_groups = schema.Tuple(
        title=_(u"Not manageable groups"),
        description=_(
            "help_gm_never_managed_groups",
            default=u"Put here a list of groups that can't be managed by users"
        ),
        required=False,
        value_type=schema.TextLine(),
        default=(
            u'Administrators',
            u'Site Administrators',
            u'Reviewers',
            u'AuthenticatedUsers',
        ),
        missing_value=(),
    )
