# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request
from odoo import tools
from odoo.tools.translate import _
from odoo.fields import Date
from odoo.exceptions import AccessError
from collections import OrderedDict

import logging
_logger = logging.getLogger(__name__)

class opennet_pricing(http.Controller):
    @http.route(['/pricing', '/opennet-pricing'], auth="public", type="http", website=True)
    def pricing(self, **kw):

        areas = request.env['ons.functionnal.area'].with_context({'lang': 'fr_FR'}).sudo().search([])

        options_logi = request.env['ons.pricing.option'].sudo().search(
            [('option_type', '=', 'logistic')]
        )
        options_misc = request.env['ons.pricing.option'].sudo().search(
            [('option_type', '=', 'misc')]
        )
        options_tech = request.env['ons.pricing.option'].sudo().search(
            [('option_type', '=', 'technical')]
        )

        hosting = request.env['ons.hosting'].sudo().search([])

        pricing = request.env['ons.user.pricing'].search([])

        values = {
            'areas': areas,
            'options_logi': options_logi,
            'options_misc': options_misc,
            'options_tech': options_tech,
            'hosting': hosting,
            'prices': pricing,
        }

        return request.render(
            "ons_cust_opennet.opennet_pricing_template", values
        )

    @http.route('/pricing/send', auth="public", type="json", methods=['POST'], website=True)
    def send_pricing(self, **post):
        name = post.get('name')
        company = post.get('company')
        email = post.get('email')
        phone = post.get('phone')
        html = post.get('html')

        request.env['ons.pricing.client'].create({
            'name': name,
            'company': company,
            'email': email,
            'phone': phone,
            'html': html,
        })

        return True