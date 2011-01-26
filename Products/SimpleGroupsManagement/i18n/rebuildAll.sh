#!/bin/sh

i18ndude rebuild-pot --pot Products.SimpleGroupsManagement.pot --create Products.SimpleGroupsManagement ..
i18ndude sync --pot Products.SimpleGroupsManagement.pot Products.SimpleGroupsManagement-??.po
