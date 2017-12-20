# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class onsUserPricing(models.Model):
    _name = 'ons.user.pricing'

    nb_user = fields.Integer(string="Number of users", required=True)
    hosting_id = fields.Many2one('ons.hosting', required=True)
    type = fields.Selection([
        ('enterprise', 'enterprise'),
        ('community', 'community'),
    ], string="Type of odoo", required=True)
    price = fields.Float(string="Price", required=True)
    name = fields.Char(string="Nom", compute='_compute_name')

    @api.multi
    def _compute_name(self):
        for pricing in self:
            pricing.name = "%s - %s - %s" % (pricing.hosting_id.name, pricing.type, pricing.nb_user)

