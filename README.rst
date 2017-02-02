Introduction
============

Have you ever feel the need to give to normal (AKA: not Manager/Site Administrator) Plone member the power to manage a group?

Right now in Plone you can make this playing with the (**Plone Site Setup: Users and Groups**).
Even playing with this permission is impossible to limit the group on which a member (or group) can manage.

This product adds a minimal configuration, a member of the site (or all members in a group) will be able to manage which users are part of a group.

You only need to go to the "*Groups management proxy settings*" settings panel.
You need to insert a set of strings like

::

    id1|group_id1
    id2|group_id2
    ...

where *id1*, *id2* can be user or group ids.
This mean that those subjects will be able to act on groups.

The utility also react to the **Add portal members** permission. If the current user has this permission you will be able to add new portal members (so no security break for this).

When an user is added or removed, an event is notified.

Compatibility
-------------

Tested with Plone 4.3 and Plone 5. Look for older releases if you need Plone 3 compatibility.

.. note::
   Right now we have **no migration** from old ( < 0.5) versions to version 0.5.
   You must manually copy/paste configuration from old portal_properties tool the new registry settings.

   If you want to provide ones: you are welcome!

TODO
----

The control panel integration user experience is a copy/paste from old ZMI portal_properties tool.
I need a hero who can find time to fix it.

Be aware!
=========

This products override all normal Plone permissions noted above! This can create **security black-holes** in your portal!

.. figure:: https://raw.githubusercontent.com/keul/Products.SimpleGroupsManagement/master/docs/Black_Hole_Milkyway.jpg
   :scale: 50

The access to the new user/group management form is still protected by the *Use Simple Groups Management* permission (commonly given to all site Members).

Credits
=======

Special thanks to Albert Pallas for being the locales-man.
