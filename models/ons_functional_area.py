# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields

class OnsFunctionnalArea(models.Model):
    _name = "ons.functionnal.area"

    name = fields.Char(string="Name")
    price = fields.Float(string="Price")
    functionnal_area_id = fields.Many2one('ons.functionnal.area')
    depend_area_ids = fields.One2many(
        'ons.functionnal.area',
        string="Depends on areas",
        inverse_name='functionnal_area_id'
    )
    app_ids = fields.Many2many('ir.module.module', string="Apps")
    logo = fields.Binary(string="Logo to upload")
    sequence = fields.Integer(string="Séquence", required=True, default=1)
