# -*- coding: utf-8 -*-
# © 2016 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class Invoice(models.Model):
    _inherit = 'account.invoice'

    last_payment_date = fields.Date(string="Last payment date", compute="_get_last_payment_date", store=True)

    @api.multi
    @api.depends('payment_move_line_ids')
    def _get_last_payment_date(self):
        for invoice in self:
            for payment in invoice.payment_move_line_ids:
                invoice.last_payment_date = payment.date

    @api.multi
    def get_grouped_taxes_values(self):
        tax_grouped = {}
        for line in self.tax_line_ids:
                val = line.amount
                key = line.name

                if key not in tax_grouped:
                    tax_grouped[key] = 0.0
                tax_grouped[key] += val

        return tax_grouped
