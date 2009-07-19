#!/bin/bash
# ensure that when something is wrong, nothing is broken more than it should...
set -e

# first, create some pot containing anything
i18ndude rebuild-pot --pot Products.SimpleGroupsManagement-generated.pot --create Products.SimpleGroupsManagement --merge manual.pot ../*
i18ndude rebuild-pot --pot plone-generated.pot --create plone --merge plone-manual.pot ../*

# then filter what we don't want, ie doubles
cp ploneboard-generated.pot Ploneboard.pot
i18ndude filter plone-generated.pot Products.SimpleGroupsManagement-generated.pot > plone-generated2.pot
## plone-plone.pot is a symbolic link (or whatever is openable on the fs) that points to PloneTranslation/i18n/plone.pot
i18ndude filter plone-generated2.pot plone-plone.pot > Products.SimpleGroupsManagement-plone.pot

# some cleaning
rm -f ploneboard-generated.pot
rm -f plone-generated.pot
rm -f plone-generated2.pot

# finally, update the po files
i18ndude sync --pot Products.SimpleGroupsManagement-plone.pot `find . -iregex '.*plone-.*\.po$'`
i18ndude sync --pot Products.SimpleGroupsManagement.pot  `find . -iregex '.*\.po$'|grep -v plone`
