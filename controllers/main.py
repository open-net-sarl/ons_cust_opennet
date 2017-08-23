# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request
from odoo import tools
from odoo.tools.translate import _
from odoo.fields import Date

import logging
_logger = logging.getLogger(__name__)


class portal_parameters(http.Controller):

    MANDATORY_FIELDS = ["email"]
    OPTIONAL_FIELDS = [
        "iban", "bank_account_number", "bvr_number", "bank_name",
        "do_email_configuration", 
        "incoming_email_server_type", "incoming_email_server_name", "incoming_email_server_port", "incoming_email_server_security", "incoming_email_server_username", "incoming_email_server_pass",
        "outgoing_email_server_name", "outgoing_email_server_port", "outgoing_email_server_security", "outgoing_email_server_username", "outgoing_email_server_password"
    ]

    @http.route(['/my/parameters'], type='http', auth='user', website=True)
    def parameters(self, **post):
        user = request.env.user
        env_config = request.env['ons.cust.customer.config']
        config = env_config.sudo().search([
            ('user_id', '=', user.id)
        ])
        values = {
            'error': {},
            'error_message': []
        }

        dict_all_options = {
            'do_email_configuration': env_config.get_do_email_configuration_options(),
            'incoming_email_server_type': env_config.get_incoming_email_server_type_options(),
            'outgoing_email_server_security': env_config.get_outgoing_email_server_security_options(),
            'sales_sale_price': env_config.get_sales_sale_price_options(),
            'accounting_last_month_fiscal_exercise': env_config.get_accounting_last_month_fiscal_exercise_options(),
            'accounting_tax_update_frequence': env_config.get_accounting_tax_update_frequence_options(),
            'stock_mng_units_mesure': env_config.get_stock_mng_units_mesure_options(),
            'stock_mng_prod_variants': env_config.get_stock_mng_prod_variants_options(),
            'stock_mng_packing_methods': env_config.get_stock_mng_packing_methods_options(),
            'stock_mng_dropshipping': env_config.get_stock_mng_dropshipping_options(),
            'stock_mng_product_owners': env_config.get_stock_mng_product_owners_options(),
            'stock_mng_expiration_dates': env_config.get_stock_mng_expiration_dates_options(),
            'stock_mng_lots_serial_nb': env_config.get_stock_mng_lots_serial_nb_options(),
        }

        if post:
            error, error_message = self.parameters_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_FIELDS if key in post})
                config.sudo().write(values)
                values.update({
                    'error': {},
                    'success': True
                })
                # return request.redirect('/my/parameters')
            else:
                values.update({
                    'success': False
                })
                

        values.update({
            'user': user,
            'config': config,
            'options_dict': dict_all_options
        })

        return request.render("ons_cust_opennet.portal_my_parameters", values)

    def parameters_form_validate(self, data):
        error = dict()
        error_message = []

        # Validation
        for field_name in self.MANDATORY_FIELDS:
            if not data.get(field_name):
                error[field_name] = 'missing'

        # email validation
        if data.get('email') and not tools.single_email_re.match(data.get('email')):
            error["email"] = 'error'
            error_message.append(_('Invalid Email! Please enter a valid email address.'))

        # error message for empty required fields
        if [err for err in error.values() if err == 'missing']:
            error_message.append(_('Some required fields are empty.'))

        unknown = [k for k in data.iterkeys() if k not in self.MANDATORY_FIELDS + self.OPTIONAL_FIELDS]
        if unknown:
            error['common'] = 'Unknown field'
            error_message.append("Unknown field '%s'" % ','.join(unknown))

        return error, error_message