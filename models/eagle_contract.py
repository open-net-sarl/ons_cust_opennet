# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class EagleContractBase(models.Model):
    _inherit = 'eagle.contract'

    # @api.onchange("customer_id", "customer_id.child_ids")
    @api.multi
    def _compute_portal_user_id(self):
        for contract in self:
            result = self.env['res.users'].search([
                ('partner_id', 'in', [c.id for c in contract.customer_id.child_ids])
            ])

            if len(result):
                contract.portal_user_id = result

    portal_user_id = fields.Many2many(
        'res.users',
        string="Portal user id",
        domain="[('partner_id', 'child_of', customer_id)]",
        compute="_compute_portal_user_id",
        store=False,
        readonly=False)


    @api.multi
    def action_contract2portalclient(self):
        list_view_id = self.env.ref('ons_cust_opennet.view_customer_config_tree').id
        form_view_id = self.env.ref('ons_cust_opennet.view_customer_config_form').id
        return {
            "type": "ir.actions.act_window",
            "res_model": "ons.cust.customer.config",
            "views": [[list_view_id, "tree"], [form_view_id, "form"]],
            "domain": [["user_id", "in", [u.id for u in self.portal_user_id]]],
            # "context": {"search_default_user_id": [self.portal_user_id.id], "default_user_id": self.portal_user_id.id},
            "name": _("Customer Portal Parameters"),
        }