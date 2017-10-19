# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields

class OnsHosting(models.Model):
    _name = 'ons.hosting'

    name = fields.Char(string="Name")
    price = fields.Float(string="Price")
    description = fields.Text(string="Description")
    logo = fields.Binary(string="Logo to upload")