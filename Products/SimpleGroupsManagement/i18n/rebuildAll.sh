#!/bin/bash
#!/bin/sh
TEMPLATES="find .. -name '*.*pt'"

i18ndude rebuild-pot --pot Products.SimpleGroupsManagement.pot --create Products.SimpleGroupsManagement $TEMPLATES 
i18ndude sync --pot Products.SimpleGroupsManagement.pot Products.SimpleGroupsManagement-ca.po
i18ndude sync --pot Products.SimpleGroupsManagement.pot Products.SimpleGroupsManagement-es.po
i18ndude sync --pot Products.SimpleGroupsManagement.pot Products.SimpleGroupsManagement-it.po
