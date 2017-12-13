# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, fields

class OnsFunctionnalArea(models.Model):
    _name = "ons.functionnal.area"
    _order = "sequence"

    name = fields.Char(string="Name")
    price = fields.Float(string="Price")
    description = fields.Html(string="Description")
    area_dependencies_id = fields.Many2one(
        'ons.dependencies.area')
    app_ids = fields.Many2many('ons.ir.module', string="Apps")
    logo = fields.Binary(string="Logo to upload")
    sequence = fields.Integer(string="Séquence", required=True)

    _sql_constraints = [
        ('sequence_uniq', 'unique (sequence)', 'Each sequence must be unique.')
    ]

class OnsAreaDependencies(models.Model):
    _name = 'ons.dependencies.area'

    @api.multi
    def _get_name(self):
        for dependencie in self:
            dependencie.name = ','.join(
                [depend.name for depend in dependencie.depend_area_ids]
            )

    name = fields.Char(string="Name", compute="_get_name")
    functionnal_area_id = fields.Many2one(
        'ons.functionnal.area',
        ondelete='set null')
    depend_area_ids = fields.Many2many(
        'ons.functionnal.area',
        string="Depends on areas",
    )
