# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    ons_user_price = fields.Float(string="Price")