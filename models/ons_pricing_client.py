# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields

class OnsPricingClient(models.Model):
    _name = 'ons.pricing.client'

    name = fields.Char(string="Nom prénom")
    company = fields.Char(string="Société")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Téléphone")
    html = fields.Html(string="html")