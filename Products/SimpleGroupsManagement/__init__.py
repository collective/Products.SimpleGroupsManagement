# -*- coding: utf-8 -*-

import logging
from zope.i18nmessageid import MessageFactory

messageFactory = MessageFactory('Products.SimpleGroupsManagement')
logger = logging.getLogger('Products.SimpleGroupsManagement')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
