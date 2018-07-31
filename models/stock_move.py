# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import datetime

import logging
_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = "stock.move"

    ons_cust_person_in_charge = fields.Many2one(
        'res.partner', 
        string='Responsable')

    # ons_order_id = fields.Many2one(related="procurement_id.sale_line_id.order_id", string="Sale Order")

    contract_id = fields.Many2one('eagle.contract', string='File')

    @api.model
    def _cron_info_person_in_charge(self):
        records = self.search([])
        jae = self.env['res.partner'].search([('ons_cust_email_two', '=', 'jae@open-net.ch')], limit=1)
        for record in records:
            date_expected = fields.Date.from_string(record.date_expected)
            if record.state in ['assigned', 'confirmed', 'waiting'] and \
               date_expected <= datetime.datetime.today().date():
                if record.picking_type_id.code == 'outgoing':
                    if record.ons_cust_person_in_charge:
                        mail_tmp = self.env.ref('ons_cust_opennet.email_template_opennet_info_cron')
                        mail_tmp.send_mail(record.id)
                    else:
                        mail_tmp = self.env.ref('ons_cust_opennet.email_template_opennet_info_cron')
                        record.ons_cust_person_in_charge = jae
                        mail_tmp.send_mail(record.id)

    @api.multi
    def info_for_mail_person_in_charge(self):
        action = self.env.ref('stock.stock_move_action') or False
        menu = self.env.ref('stock.menu_stock_root') or False
        date_expected = fields.Date.from_string(self.date_expected)
        return {'action': action,'menu': menu, 'date_expected': date_expected}

    @api.model
    def create(self, values):
        new_move = super(StockMove, self).create(values)
        # if new_move and new_move.procurement_id:
        #     new_move.contract_id = new_move.procurement_id.eagle_contract

        return new_move
