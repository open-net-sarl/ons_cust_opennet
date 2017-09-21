# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = "stock.move"

    ons_cust_person_in_charge = fields.Many2one(
        'res.partner', 
        string='Responsable')

    @api.model
    def _cron_info_person_in_charge(self):
        records = self.search([])
        for record in records:
            if record.ons_cust_person_in_charge:
                _logger.info("FOUND STOCK MOVE W/ PIC")

                # https://github.com/search?l=Python&q=org%3AOCA+generate_email&type=Code
                # mail.py ledixa 