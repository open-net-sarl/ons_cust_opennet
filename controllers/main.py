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
from odoo.addons.website_portal.controllers.main import website_account
from odoo.addons.website_project.controllers.main import WebsiteAccount

import logging
_logger = logging.getLogger(__name__)


class portal_parameters(http.Controller):

    MANDATORY_FIELDS = ["email"]

    OPTIONAL_FIELDS = [
        # Bank Info
        "iban", "bank_account_number", "bvr_number", 
        "bank_name", "bank_agency_name",

        # Configurations
        "do_email_configuration", 

        # Incoming Email Server
        "incoming_email_server_type", "incoming_email_server_name", "incoming_email_server_port", 
        "incoming_email_server_security", "incoming_email_server_username", "incoming_email_server_pass",

        # Outgoing Email Server
        "outgoing_email_server_name", "outgoing_email_server_port", "outgoing_email_server_security",
        "outgoing_email_server_username", "outgoing_email_server_password",

        # Document Numbering
        "doc_numb_quot_sales", "doc_numb_invoices", "doc_numb_purchases", 
        "doc_numb_delivery",

        # Contact Default Parameters
        "contacts_lang", "contacts_payment_terms",

        # Product Default Parameters
        "products_type", "products_can_be_sold", "products_can_be_purchased", 
        "products_warranty", "products_delivery_delay", "products_earnings_acc", 
        "products_spendings_acc", "products_customer_tax", "products_supplier_tax", 
        "products_supply_routes", "products_unit_of_mesure",

        # Sales Parameters
        "sales_sale_price", "sales_invoicing_policy", "sales_general_conditions", 
        "sales_authorize_different_address", "sales_modify_sale_order",

        # Accounting Default Parameters
        "accounting_last_day_fiscal_exercise", "accounting_last_month_fiscal_exercise", "accounting_currency", 
        "accounting_analytic_acc", "accounting_asset_management", "accounting_revenu_recognition", 
        "accounting_budget_management", "accounting_output_bvr", "accounting_iso_payment", 
        "accounting_foreign_currencies_list", "accounting_tax_update_frequence", "accounting_reminder_levels",

        # Stock Management Default Parameters
        "stock_mng_units_mesure", "stock_mng_prod_variants", "stock_mng_packing_methods",
        "stock_mng_dropshipping", "stock_mng_generate_journal_item", "stock_mng_product_owners",
        "stock_mng_expiration_dates", "stock_mng_lots_serial_nb"
    ]

    # convert values from the checkboxes
    CHECKBOX_FIELDS = [
        # Incoming Email Server
        "incoming_email_server_security", 
        # Product Default Parameters
        "products_can_be_sold", "products_can_be_purchased", 
        # Sales Parameters
        "sales_authorize_different_address",
        # Accounting Default Parameters
        "accounting_analytic_acc", "accounting_asset_management", "accounting_revenu_recognition", 
        "accounting_budget_management", "accounting_output_bvr", "accounting_iso_payment", 
        "accounting_foreign_currencies_list", "accounting_reminder_levels",
        # Stock Management Default Parameters
        "stock_mng_generate_journal_item"
    ]

    @http.route(['/my/parameters'], type='http', auth='user', website=True)
    def parameters(self, **post):
        user = request.env.user
        env_config = request.env['ons.cust.customer.config']
        config = env_config.sudo().search([
            ('user_id', '=', user.id)
        ])
        if not len(config):
            env_config.sudo().create({'user_id': user.id})
            return request.redirect('/my/parameters')

        values = {
            'error': {},
            'error_message': []
        }

        # Contact Default Parameters
        all_langs = request.env['res.lang'].sudo().search(['|', ('active', '=', False), ('active', '=', True )])
        lang_options = [(lang.id, lang.name) for lang in all_langs]
        all_payment_terms = request.env['account.payment.term'].sudo().search([])
        payment_terms_options = [(term.id, term.name) for term in all_payment_terms]

        # Product Default Parameters
        all_customer_taxes = request.env['account.tax'].sudo().search([('type_tax_use', '=', 'sale')])
        customer_taxes_options = [(tax.id, tax.name) for tax in all_customer_taxes]
        all_supplier_taxes = request.env['account.tax'].sudo().search([('type_tax_use', '=', 'purchase')])
        supplier_taxes_options = [(tax.id, tax.name) for tax in all_supplier_taxes]
        all_product_uoms = request.env['product.uom'].sudo().search([])
        product_uoms_options = [(uom.id, uom.name) for uom in all_product_uoms]

        # Accounting Default Parameters
        all_currencies = request.env['res.currency'].sudo().search(['|', ('active', '=', False), ('active', '=', True )])
        currency_options = [(currency.id, currency.name) for currency in all_currencies]

        # all the options for the website selects
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
            'products_type': env_config.get_products_type_options(),
            'contacts_lang': lang_options,
            'contacts_payment_terms': payment_terms_options,
            'products_customer_tax': customer_taxes_options,
            'products_supplier_tax': supplier_taxes_options,
            'products_unit_of_mesure': product_uoms_options,
            'accounting_currency': currency_options
        }

        if post:
            # convert values from the checkboxes
            for field_check in self.CHECKBOX_FIELDS:
                if field_check in post:
                    post[field_check] = True
                else:
                    post[field_check] = False

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

class website_account(website_account):

    MANDATORY_BILLING_FIELDS = ["phone", "email", "street", "city", "country_id"]

    def _prepare_portal_layout_values(self):
        values = super(website_account, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        StockPicking = request.env['stock.picking']
        StockMove = request.env['stock.move'].sudo()

        domain_pickings = ['|', ('partner_id', '=', partner.commercial_partner_id.id),('partner_id', '=', partner.id)]
        domain_moves = ['|', ('partner_id', '=', partner.commercial_partner_id.id),('partner_id', '=', partner.id)]

        all_stock_picking = StockPicking.sudo().search(domain_pickings)
        all_stock_move = StockMove.sudo().search(domain_moves)

        pickings_count = len([picking.id for picking in all_stock_picking])
        moves_count = len([move.id for move in all_stock_move])

        values.update({
            'pickings_count': pickings_count,
            'moves_count': moves_count,
        })
        return values

    @http.route(['/my/deliveries', '/my/deliveries/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_stock_picking(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        StockPicking = request.env['stock.picking'].sudo()

        # domain_pickings = domain
        domain_pickings = ['|', ('partner_id', '=', partner.commercial_partner_id.id),('partner_id', '=', partner.id)]

        all_stock_picking = StockPicking.sudo().search(domain_pickings)

        # count for pager
        pickings_count = len([picking.id for picking in all_stock_picking])

        archive_groups = self._get_archive_groups('stock.picking', domain_pickings)
        # pager
        pager = request.website.pager(
            url="/my/deliveries",
            total=pickings_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        stock_pickings = StockPicking.sudo().search(domain_pickings, limit=self._items_per_page, offset=pager['offset'])
        # values
        values.update({
            'stock_pickings': stock_pickings,
            'page_name': 'Stock',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/deliveries',
        })
        return request.render("ons_cust_opennet.portal_my_stock_picking", values)

    @http.route(['/my/deliveries/<int:picking_id>'], type='http', auth="user", website=True)
    def pickings_followup(self, picking_id=None, **kw):
        picking = request.env['stock.picking'].browse([picking_id])
        try:
            picking.check_access_rights('read')
            picking.check_access_rule('read')
        except AccessError:
            return request.render("website.403")

        return request.render("ons_cust_opennet.pickings_followup", {
            'picking': picking
        })

    @http.route(['/my/moves', '/my/moves/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_stock_move(self, page=1, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        StockMove = request.env['stock.move'].sudo()

        domain_moves = ['|', ('partner_id', '=', partner.commercial_partner_id.id),('partner_id', '=', partner.id)]

        all_stock_move = StockMove.sudo().search(domain_moves)

        # count for pager
        moves_count = len([move.id for move in all_stock_move])
        _logger.info('move count %s' % moves_count)

        archive_groups = self._get_archive_groups('stock.move', domain_moves)
        # pager
        pager = request.website.pager(
            url="/my/moves",
            total=moves_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        stock_moves = StockMove.sudo().search(domain_moves, limit=self._items_per_page, offset=pager['offset'], order='date desc')
        _logger.info('stock move %s' % stock_moves)
        # values
        values.update({
            'stock_moves': stock_moves,
            'page_name': 'Moves',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/my/moves',
        })
        return request.render("ons_cust_opennet.portal_my_stock_move", values)

    @http.route(['/my/moves/<int:move_id>'], type='http', auth="user", website=True)
    def moves_followup(self, move_id=None, **kw):
        move = request.env['stock.move'].browse([move_id])
        try:
            move.check_access_rights('read')
            move.check_access_rule('read')
        except AccessError:
            return request.render("website.403")

        return request.render("ons_cust_opennet.moves_followup", {
            'move': move
        })


class WebsiteAccount(WebsiteAccount):

    def _prepare_portal_layout_values(self):
        values = super(WebsiteAccount, self)._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        project_count = request.env['project.project'].search_count([('privacy_visibility','=','portal')])
        task_count = request.env['project.task'].sudo().search_count([('project_id.privacy_visibility','=','portal'), '|', ('partner_id', '=', partner.commercial_partner_id.id),('partner_id', '=', partner.id)])
        values.update({
            'project_count': project_count,
            'task_count': task_count,
        })
        return values

    @http.route(['/my/tasks', '/my/tasks/page/<int:page>'], type='http', auth="user", website=True)
    def my_tasks(self, page=1, date_begin=None, date_end=None, project=None, sortby=None, **kw):
        _logger.info('********************MY TASKS ooooo*******************')
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id

        sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
        }

        projects = request.env['project.project'].search([('privacy_visibility', '=', 'portal')])

        project_filters = {
            'all': {'label': _('All'), 'domain': []},
        }

        for proj in projects:
            project_filters.update({
                str(proj.id): {'label': proj.name, 'domain': [('project_id', '=', proj.id)]}
            })

        domain = [('project_id.privacy_visibility', '=', 'portal')]
        domain += project_filters.get(project, project_filters['all'])['domain']
        order = sortings.get(sortby, sortings['date'])['order']
        domain += ['|', ('partner_id', '=', partner.commercial_partner_id.id),('partner_id', '=', partner.id)]

        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups('project.task', domain)
        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # pager
        pager = request.website.pager(
            url="/my/tasks",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'project': project},
            total=values['task_count'],
            page=page,
            step=self._items_per_page
        )

        _logger.info(domain)
        # content according to pager and archive selected
        tasks = request.env['project.task'].sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'project_filters': OrderedDict(sorted(project_filters.items())),
            'projects': projects,
            'project': project,
            'sortings': sortings,
            'sortby': sortby,
            'tasks': tasks,
            'page_name': 'task',
            'archive_groups': archive_groups,
            'default_url': '/my/tasks',
            'pager': pager
        })
        return request.render("website_project.my_tasks", values)

    @http.route(['/my/task/<model("project.task"):task>'], type='http', auth="user", website=True)
    def my_task(self, task=None, **kw):
        try:
            task.check_access_rights('read')
            task.check_access_rule('read')
        except AccessError:
            return request.render("website.403")

        return request.render("website_project.my_task", {'task': task, 'user': request.env.user})

class opennet_price(http.Controller):
    """docstring for ClassName"""
    @http.route(['/opennet-pricing'], auth="public", type="http", website=True)
    def pricing(self, **kw):

        areas = request.env['ons.functionnal.area'].search([])
        options_logi = request.env['ons.pricing.option'].search(
            [('option_type', '=', 'logistic')]
        )
        options_misc = request.env['ons.pricing.option'].search(
            [('option_type', '=', 'misc')]
        )
        options_tech = request.env['ons.pricing.option'].search(
            [('option_type', '=', 'technical')]
        )

        hosting = request.env['ons.hosting'].search([])

        ons_user_price = request.env['res.company'].search_read(
            [], fields=['ons_user_price']
        )

        values = {
            'areas': areas,
            'options_logi': options_logi,
            'options_misc': options_misc,
            'options_tech': options_tech,
            'hosting': hosting,
            'user_price': ons_user_price,
        }

        return request.render(
            "ons_cust_opennet.opennet_pricing_template", values
        )
