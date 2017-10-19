# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields

class OnsPricingOption(models.Model):
    _name = "ons.pricing.option"

    name = fields.Char(string="Name")
    price = fields.Float(string="Price")
    app_ids = fields.Many2many('ir.module.module', string="Apps")
    logo = fields.Binary(string="Logo to upload")
    option_type = fields.Selection([
        ('logistic', 'Intégration logistique'),
        ('technical', 'Outils techniques'),
        ('misc', 'Divers'),
    ])
