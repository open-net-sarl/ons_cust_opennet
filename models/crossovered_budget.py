# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"
    _description = "Budget Line"

    @api.multi
    def _compute_practical_amount(self):

        for line in self:
            result = 0.0
            acc_ids = line.general_budget_id.account_ids.ids
            if not acc_ids:
                raise UserError(_("The Budget '%s' has no accounts!") % ustr(line.general_budget_id.name))
            date_to = self.env.context.get('wizard_date_to') or line.date_to
            date_from = self.env.context.get('wizard_date_from') or line.date_from

            '''
                removed mandatory from analytic_account and search with it
            '''

            self.env.cr.execute("""
                SELECT SUM(credit), SUM(debit)
                FROM account_move_line
                WHERE (date between to_date(%s,'yyyy-mm-dd') AND to_date(%s,'yyyy-mm-dd'))
                    AND account_id=ANY(%s)""",
            (date_from, date_to, acc_ids,))

            fetch_result = self.env.cr.fetchone()
            # _logger.info(fetch_result)
            result = (fetch_result[0] - fetch_result[1]) or 0.0
            # _logger.info(result)
            line.practical_amount = result