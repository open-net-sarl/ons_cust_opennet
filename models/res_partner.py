# -*- coding: utf-8 -*-
# © 2016 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    ons_cust_email_two = fields.Char(string="ONS Email")

    @api.model
    def _deduplicate_tags_on_partner(self):
        records = self.search([])
        for record in records:
            tag_ids = []
            for tag in record.category_id:
                if tag.id not in tag_ids:
                    tag_ids.append(tag.id)

            record.write({'category_id':[(6,0,tag_ids)]})