# -*- coding: utf-8 -*-
# © 2016 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class MassMailing(models.Model):
    _name = 'mail.mass_mailing'
    _inherit = ['mail.mass_mailing', 'mail.thread']