# -*- coding: utf-8 -*-
# © 2016 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models


class crm_lead(models.Model):
    _inherit = 'crm.lead'

    _order = 'create_date DESC'