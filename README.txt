Introduction
============

Have you ever feel the need to give to normal (AKA: not Manager/Site Administrator ) Plone member the power to
manage a group?

Right now in Plone you can make this possible playin with the **Manage users** and **Manage Groups**.

Even playing with those permissions is impossible is to limit the group on which a member (or group of members)
can manage.

This products make something very dangerous: with a minimal configuration, a member of the Plone portal
(or all members in a group) will be able to manage the users of a group overriding the basic portal security.
You only need to go to the *portal_properties* tool of you portal and modifiy the new
**simple_groups_management_properties**.

In the *sgm_data* section you need to insert a set of strings like

::

    id1|group_id1
    id2|group_id2
    ...

where *id1*, *id2* can be user or group ids. This mean that the member (or group) id1 will be able to act on the
group_id1 members.

You can also insert a list of groups ids that will be never handled by this product in the
**sgm_never_managed_groups** section.

The utility also react to the **Add portal members** permission. If the current user has this permission
you will be able to add new portal members (so no security break for this).

When an user is added to a group or removed, an event will be raised.

Be aware!
---------

This products override all normal Plone permissions noted above! This can create **security black-holes** in
your portal!

.. figure:: http://keul.it/images/Black_Hole_Milkyway.jpg
   :scale: 50

The access to the new user/group management form is protected by the **Use Simple Groups Management**
permission (commonly given to all site Members).

Similar product
---------------

Maybe is a good idea to check also `collective.groupdelegation`__

__ http://pypi.python.org/pypi/collective.groupdelegation

TODO
----

* Don't force the Manager to go in ZMI, but handle configuration from Plone UI.
* Some portalMessage doesn't work correctly.

Credits
-------

Special thanks to Albert Pallas for beeing the locales-man.
