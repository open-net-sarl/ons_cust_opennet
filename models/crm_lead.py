# -*- coding: utf-8 -*-
# © 2016 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, api, fields
from datetime import datetime, timedelta


class crm_lead(models.Model):
    _inherit = 'crm.lead'

    _order = 'last_message_date DESC, create_date DESC'

    @api.depends('message_ids.date')
    def _get_last_message_date(self):
        for lead in self:
            messages = sorted(lead.message_ids, key=lambda message: message.date)
            if messages:
                lead.last_message_date = messages[-1].date

    @api.depends('message_ids.date')
    def _has_recent_messages(self):
        for lead in self:
            lead.has_recent_messages = False
            for message in lead.message_ids:
                if fields.Datetime.from_string(message.date) >= datetime.today() - timedelta(days=3):
                    lead.has_recent_messages = True

    last_message_date = fields.Datetime(string="Date du dernier message", compute="_get_last_message_date", store=True)
    has_recent_messages = fields.Boolean(compute="_has_recent_messages", store=True)