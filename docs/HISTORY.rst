Changelog
=========

0.7.0 (unreleased)
------------------

- Changes to Python 3 and Plone 5.2.
  Plone 4 should work too. Plone 3 is probably gone forever.
  [keul]


0.6.0 (2017-02-03)
------------------

- New feature: mass add members providing a file
  [keul]


0.5.0 (2017-02-02)
------------------

Plone 5 compatibility

- Moved i18n to locales (some translation has been lost due to strange encoding issues)
  [keul]
- Added a configuration registry panel and moved to plone.app.registry
  [keul]
- Fixed form GET to POST
  [keul]
- Fixed an issue that allow user management for groups with similar names
  [keul]
- Update load user code as Plone controlpanel do; this fix LDAP integration issue
  [keul]
- Fix accents in spanish translations.
  [cekk]


0.4.1 (2013-11-15)
------------------

- Standardise markup as per https://dev.plone.org/ticket/10231 [davismr]
- Fixed permission problem when user has empty list of groups [davismr]
- Fixed group management form format and labels [keul]
- Show usernames [keul]

0.4.0 (2012-10-04)
------------------

* Added support for the Site Administrator role [keul]
* Moved action link to manage groups from portal_action to
  user section (in the proper Plone 4 style way) [keul]
* Added a proper uninstall procedure [keul]
* Updated templates to Plone 4 [keul]
* Added a project browserlayer [keul]
* Added missing translation strings [keul]
* HTML 5 fixes [keul]
* Search also by userid [keul]
* Fixed portal message problem [keul]

0.3.2 (2011/12/19)
------------------

* Added title of the group in groups listing [micecchi]

0.3.1 (2011/07/12)
------------------

* fixed bug in group listing [micecchi]

0.3.0 (2011/07/10)
------------------

* No more Plone 2.5 support
* Plone UI updated to Plone 3 world [micecchi]
* Moved tool-link from users preferences to plone_control_panel [micecchi]
* Created a link in site_actions to access the management view [micecchi]
* Created a custom event raised when an user is assigned/deleted to a group
  when using this product [micecchi]
* Changed the way of listing users, to support ldap and many users [micecchi]
* Improved Plone 4 compatibility [micecchi]

0.2.0
-----

* Albert Pallas provided internationalization support
* Again Albert added catalan, spanish and french translations
* Added italian translation

0.1.0
-----

* Initial release
