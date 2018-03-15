# -*- coding: utf-8 -*-
# © 2018 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class EventEvent(models.Model):
    _inherit = 'event.event'

    @api.multi
    def copy(self, default=None):
        res = super(EventEvent, self).copy(default)
        res.event_mail_ids.write({
            'mail_sent': False,
            'done': False
        })
        return res
