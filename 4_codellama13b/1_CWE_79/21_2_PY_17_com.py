from five import grok
from zope.i18nmessageid import MessageFactory
from html import escape

PMF = MessageFactory('plone')

grok.templatedir('templates')


def renderCell(self, item):
    value = get_value(item, self.attribute, default=())

    if not isinstance(value, (list, tuple)):
        value = (value,)

    gtool = getToolByName(plone.api.portal.get(), 'portal_groups')
    mtool = getToolByName(plone.api.portal.get(), 'portal_membership')
    principals = []
    for principal_id in value:
        user = mtool.getMemberById(principal_id)
        if user is not None:
            principals.append(escape(user.getProperty('fullname', None)) or user.getId())
        else:
            group = gtool.getGroupById(principal_id)
            if group is not None:
                # the following code is for fixing the vulnerability CWE-79 (Cross-site Scripting)
                # https://cwe.mitre.org/data/definitions/79.html
                principals.append(escape(group.getProperty('title', None)) or group.getId())
            else:
                principals.append(principal_id)
    return ', '.join(principals