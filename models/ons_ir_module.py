# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields

class onsIrModule(models.Model):
	_name = 'ons.ir.module'

	name = fields.Char(string="Name")
	shortdesc = fields.Text(string="Shortdesc")
	description = fields.Text(string="Description")
	logo = fields.Binary("Logo")
	license = fields.Selection([
        ('enterprise', '(E)'),
        ('community', '(C)'),
    ], required=True)
