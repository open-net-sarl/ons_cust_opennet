# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _
from odoo.exceptions import AccessError
from odoo.tools.safe_eval import safe_eval

#Import logger
import logging
#Get the logger
_logger = logging.getLogger(__name__)

class ProjectIssue(models.Model):
    _inherit = 'project.issue'

    @api.multi
    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, subtype=None,parent_id=False, **kwargs):
        cc_partner_ids = ', '.join([partner.name for partner in self.message_partner_ids if partner.email != 'support@open-net.ch'])
        send_to = u"Envoyé également à " + cc_partner_ids
        kwargs['body'] = tools.append_content_to_html(kwargs['body'], send_to, container_tag='div')
        mail_message = super(ProjectIssue, self).message_post(subtype=subtype, **kwargs)
        return mail_message