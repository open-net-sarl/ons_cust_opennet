# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

import csv
import base64
import datetime

class EagleContractBase(models.Model):
    _inherit = 'eagle.contract'

    lst_stock_moves = fields.One2many(
        'stock.move',
        inverse_name='contract_id',
        string='Stock moves'
    )

#     stock_moves = fields.One2many(
#         'stock.move', inverse_name='contract_id', readonly=True, compute='_detect_stock_moves', string='Stock moves', 
#     store=False )
#
#     def _detect_stock_moves(self):
#         for cnt in self:
#             lst = [] for sale in cnt.current_sale_orders + cnt.past_sale_orders:
#                 lst += [] if not sale.procurement_group_id else \
#                     self.env['stock.move'].search([('group_id','=',sale.procurement_group_id.id)]) cnt.stock_moves = [x.id 
#             for x in lst]

    # @api.onchange("customer_id", "customer_id.child_ids")
    @api.multi
    def _compute_portal_user_ids(self):
        for contract in self:
            result = self.env['res.users'].search([
                ('partner_id', 'in', [c.id for c in contract.customer_id.child_ids])
            ])

            if len(result):
                contract.portal_user_ids = result

    portal_user_ids = fields.Many2many(
        'res.users',
        string="Portal user id",
        domain="[('partner_id', 'child_of', customer_id)]",
        compute="_compute_portal_user_ids",
        store=False,
        readonly=False)


    @api.multi
    def action_contract2portalclient(self):
        self.ensure_one()
        list_view_id = self.env.ref('ons_cust_opennet.view_customer_config_tree').id
        form_view_id = self.env.ref('ons_cust_opennet.view_customer_config_form').id
        return {
            "type": "ir.actions.act_window",
            "res_model": "ons.cust.customer.config",
            "views": [[list_view_id, "tree"], [form_view_id, "form"]],
            "domain": [["user_id", "in", [u.id for u in self.portal_user_ids]]],
            "name": _("Customer Portal Parameters"),
        }

    @api.multi
    def action_contract2customerchanges(self):
        self.ensure_one()
        tree_view_id = self.env.ref('ons_cust_opennet.view_customer_changes_tree').id
        form_view_id = self.env.ref('ons_cust_opennet.view_customer_changes_form').id
        return {
            "type": "ir.actions.act_window",
            "res_model": "mail.message",
            "views": [[tree_view_id, "tree"], [form_view_id, "form"]],
            "domain": [["ons_partner_id", "=", self.customer_id.id]],
            "name": _("Customer Portal Changes"),
        }

        
    @api.multi
    def export_email(self):
        FILENAME = "partner_emails_" + datetime.datetime.now().strftime("%Y-%m-%d") + ".csv"
        emails = []

        # Select 'Ongoing' contract
        contracts = self.search([('state', 'ilike', 'production')]) 
        emails.append(['client_name', 'client_vm_name', 'client_email'])
        for contract in contracts:
            client_name = unicode(contract.name).encode('utf-8')
            vm_name = str(contract.category_id.name)
            client_email = str(contract.customer_id.email)
            
            emails.append([client_name, vm_name, client_email])

        # Concert 2D array to csv string
        emails_csv_string = '\n'.join(map(lambda row: ','.join(map(str, row)), emails))

        attachment = {
            'name': ("Patner emails"),
            'datas': base64.b64encode(emails_csv_string),
            'datas_fname': FILENAME,
            'type': 'binary'
        }

        attachment_ref = self.env['ir.attachment'].create(attachment)

        mail = self.env.ref('ons_cust_opennet.extract_email')
        mail.attachment_ids =  False
        mail.attachment_ids =  [(4,attachment_ref.id)]


        mail.send_mail(273)

    @api.multi
    def action_send_contract_email(self):
        self.ensure_one()

        template = self.env.ref('ons_cust_opennet.email_template_eagle_contract', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)

        context = dict(
            default_model='eagle.contract',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            force_email=True
        )

        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': context,
        }