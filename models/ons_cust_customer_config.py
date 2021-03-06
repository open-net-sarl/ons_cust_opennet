# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def create(self, vals):
        res = super(ResUsers, self).create(vals)

        # different at every db
        portal_group = self.env.ref('base.group_portal')
        # _logger.info("PORTAL GROUP ID: %s" % portal_group.id)
        if vals['in_group_'+str(portal_group.id)]:
            self.env['ons.cust.customer.config'].create({'user_id': res.id})
        return res

class MailMessage(models.Model):
    """docstring for MailMessage"""
    _inherit = "mail.message"

    @api.multi
    def _get_tracking_values(self):
        tracking_values = ''
        for message in self:
            for track in message.tracking_value_ids:
                _logger.info('track.field_desc %s' % track.field_desc)
                tracking_values += track.field_desc
                tracking_values += ' : '
                new_display_value = track.get_new_display_value()[0]
                old_display_value = track.get_old_display_value()[0]
                if old_display_value:
                    tracking_values = "%s %s" % (tracking_values, old_display_value)
                if new_display_value:
                    if old_display_value != new_display_value:
                        tracking_values = "%s -> %s" % (tracking_values, new_display_value)
                    tracking_values += '\n'
            message.ons_tracking_values = tracking_values

    ons_tracking_values = fields.Text(
        string="Tracking values",
        compute="_get_tracking_values"
    )

    @api.depends('tracking_value_ids')
    def _get_partner_id(self):
        for message in self:
            if message.res_id:
                related_object = self.env[message.model].browse(message.res_id)
                if related_object:
                    if hasattr(related_object, "partner_id"):
                        if related_object.partner_id.parent_id:
                            message.ons_partner_id = related_object.partner_id.parent_id.id
                        else:
                            message.ons_partner_id = related_object.partner_id.id

    ons_partner_id = fields.Many2one(
        'res.partner',
        compute="_get_partner_id",
        store=True,
        string="Partner id"
    )

class OnsCustCustomerConfig(models.Model):
    _name = "ons.cust.customer.config"

    _inherit = ['mail.thread']

    user_id = fields.Many2one(
        'res.users',
        string='Customer',
        required=True,
        readonly=True)

    partner_id = fields.Many2one(
        'res.partner',
        related='user_id.partner_id'
    )

    name = fields.Char(
        string="Name",
        related='user_id.display_name')

    eagle_contracts = fields.Many2many(
        string="Eagle Contracts",
        related="user_id.eagle_contracts")

    # - SELECTION GETS -
    @api.model
    def get_do_email_configuration_options(self):
        options = [
            ('none', _('None')),
            ('in', _('Incoming Server')),
            ('out', _('Outgoing Server')),
            ('all', _('Incoming and Outgoing Servers'))
        ]
        return options

    @api.model
    def get_incoming_email_server_type_options(self):
        options = [
            ('pop', _('POP Server')),
            ('imap', _('IMAP Server')),
        ]
        return options

    @api.model
    def get_outgoing_email_server_security_options(self):
        options = [
            ('none', _('None')),
            ('starttls', _('TLS (STARTTLS)')),
            ('ssl', _('SSL/TLS'))
        ]
        return options

    @api.model
    def get_sales_sale_price_options(self):
        options = [
            ('fixed', _('A single sale price per product')),
            ('percentage', _('Specific prices per customer segment, currency, etc.')),
            ('formula', _('Advanced pricing based on formulas (discounts, margins, rounding)'))
        ]
        return options

    @api.model
    def get_accounting_last_month_fiscal_exercise_options(self):
        options = [
            ('1', _('January')), ('2', _('February')), ('3', _('March')), 
            ('4', _('April')), ('5', _('May')), ('6', _('June')), 
            ('7', _('July')), ('8', _('August')), ('9', _('September')), 
            ('10', _('October')), ('11', _('November')), ('12', _('December'))
        ]
        return options

    @api.model
    def get_accounting_tax_update_frequence_options(self):
        options = [
            ('manually', _('Manually')),
            ('daily', _('Daily')),
            ('weekly', _('Weekly')),
            ('monthly', _('Monthly'))
        ]
        return options

    @api.model
    def get_stock_mng_units_mesure_options(self):
        options = [
            ('0', _('Products have only one unit of measure (easier)')),
            ('1', _('Some products may be sold/purchased in different units of measure (advanced)'))
        ]
        return options

    @api.model
    def get_stock_mng_prod_variants_options(self):
        options = [
            ('0', _('No variants on products')),
            ('1', _('Products can have several attributes, defining variants (Example: size, color,...)'))
        ]
        return options

    @api.model
    def get_stock_mng_packing_methods_options(self):
        options = [
            ('0', _('Do not manage packaging')),
            ('1', _('Manage available packaging options per products'))
        ]
        return options

    @api.model
    def get_stock_mng_dropshipping_options(self):
        options = [
            ('0', _('Suppliers always deliver to your warehouse(s)')),
            ('1', _('Allow suppliers to deliver directly to your customers'))
        ]
        return options

    @api.model
    def get_stock_mng_product_owners_options(self):
        options = [
            ('0', _('All products in your warehouse belong to your company')),
            ('1', _('Manage consignee stocks (advanced)'))
        ]
        return options

    @api.model
    def get_stock_mng_expiration_dates_options(self):
        options = [
            ('0', _('Do not use Expiration Date on serial numbers')),
            ('1', _('Define Expiration Date on serial numbers'))
        ]
        return options

    @api.model
    def get_stock_mng_lots_serial_nb_options(self):
        options = [
            ('0', _('Do not track individual product items')),
            ('1', _('Track lots or serial numbers'))
        ]
        return options

    @api.model
    def get_products_type_options(self):
        options = [
            ('consu', _('Consumable')),
            ('service', _('Service')),
            ('product', _('Stockable Product'))
        ]
        return options
    # - END SELECTION GETS -

    # - Votre Société - #
    # company info
    logo = fields.Binary(
        'Logo (vectorial)', 
        attachment=True, 
        track_visibility='onchange'
    )
    logo_name = fields.Char(
        'Logo Name', 
        track_visibility='onchange'
    )
    email = fields.Char(
        "Administrator's Email", 
        track_visibility='onchange'
    )

    # bank info
    iban = fields.Char('IBAN', track_visibility='onchange')
    bank_account_number = fields.Char('Bank Account Number', track_visibility='onchange')
    bvr_number = fields.Char('BVR Number', track_visibility='onchange')
    bank_name = fields.Char('Bank Name', track_visibility='onchange')
    bank_agency_name = fields.Char(
        'Bank Agency Name (local)',
        track_visibility='onchange'
    )
    # - END - #

    # - Configurations - #
    do_email_configuration = fields.Selection(
        get_do_email_configuration_options,
        default='none',
        string="Do email configuration for",
        track_visibility='onchange'
    )
    # serveur d'email entrant - Incoming Email Server
    incoming_email_server_type = fields.Selection(
        get_incoming_email_server_type_options, 
        default='pop', 
        string="Server Type", 
        track_visibility='onchange'
    )
    incoming_email_server_name = fields.Char(
        "Server Name", 
        help="Hostname or IP of the mail server", 
        track_visibility='onchange'
    )
    incoming_email_server_port = fields.Char("Port", track_visibility='onchange')
    incoming_email_server_security = fields.Boolean(
        "Security SSL/TLS", 
        help="Connections are encrypted with SSL/TLS through a dedicated port (default: IMAPS=993, POP3S=995)",
        track_visibility='onchange'
    )
    incoming_email_server_username = fields.Char("Username", track_visibility='onchange')
    incoming_email_server_pass = fields.Char("Password", track_visibility='onchange')

    # serveur d'email sortant - Outgoing Email Server
    outgoing_email_server_name = fields.Char("SMTP Server",
        help="Hostname or IP of SMTP server",
        track_visibility='onchange'
    )
    outgoing_email_server_port = fields.Char(
        "SMTP Port", 
        default=25, 
        help="SMTP Port. Usually 465 for SSL, and 25 or 587 for other cases.", 
        track_visibility='onchange'
    )
    outgoing_email_server_security = fields.Selection(
        get_outgoing_email_server_security_options, default='none', string="Security", 
        help="Choose the connection encryption scheme:\n"
            "- None: SMTP sessions are done in cleartext.\n"
            "- TLS (STARTTLS): TLS encryption is requested at start of SMTP session (Recommended)\n"
            "- SSL/TLS: SMTP sessions are encrypted with SSL/TLS through a dedicated port (default: 465)", 
            track_visibility='onchange')
    outgoing_email_server_username = fields.Char(
        "Username", 
        help="Optional username for SMTP authentication", 
        track_visibility='onchange'
    )
    outgoing_email_server_password = fields.Char("Password", track_visibility='onchange')

    # numerotation de vos documents - Document Numbering
    doc_numb_quot_sales = fields.Char("Quotations & Sales", track_visibility='onchange')
    doc_numb_invoices = fields.Char("Invoices", track_visibility='onchange')
    doc_numb_purchases = fields.Char("Purchase Orders", track_visibility='onchange')
    doc_numb_delivery = fields.Char("Delivery Orders", track_visibility='onchange')

    # carnet d'adress - Contact Default Parameters
    contacts_lang = fields.Many2one(
        'res.lang',
        string="Language",
        track_visibility='onchange')
    contacts_payment_terms = fields.Many2one(
        'account.payment.term',
        string='Payment Terms',
        help="This payment term will be used instead of the default one for sale orders and customer invoices",
        track_visibility='onchange')

    # articles - Product Default Parameters
    products_type = fields.Selection(
        get_products_type_options, 
        "Product Type", 
        track_visibility='onchange'
    )
    products_can_be_sold = fields.Boolean("Can Be Sold", track_visibility='onchange')
    products_can_be_purchased = fields.Boolean("Can Be Purchased", track_visibility='onchange')
    products_warranty = fields.Integer("Warranty (months)", track_visibility='onchange')
    products_delivery_delay = fields.Integer("Delivery Delay to the Customer (days)", track_visibility='onchange')
    products_earnings_acc = fields.Char("Earnings Account", track_visibility='onchange')
    products_spendings_acc = fields.Char("Spendings Account", track_visibility='onchange')
    products_customer_tax = fields.Many2one(
        'account.tax', 
        string="Customer Tax", 
        domain=[('type_tax_use', '=', 'sale')], 
        track_visibility='onchange'
    )
    products_supplier_tax = fields.Many2one(
        'account.tax', 
        string="Supplier Tax", 
        domain=[('type_tax_use', '=', 'purchase')], 
        track_visibility='onchange'
    )
    products_supply_routes = fields.Char("Supply Routes", track_visibility='onchange')
    products_unit_of_mesure = fields.Many2one('product.uom', string="Unit of Mesure", track_visibility='onchange')

    # ventes - Sales Parameters
    sales_sale_price = fields.Selection(
        get_sales_sale_price_options, default='fixed', string="Sale Price",
        help='Fix Price: all price manage from products sale price.\n'
             'Different prices per Customer: you can assign price on buying of minimum quantity in products sale tab.\n'
             'Advanced pricing based on formula: You can have all the rights on pricelist',
             track_visibility='onchange')
    sales_invoicing_policy = fields.Char("Invoicing Policy", track_visibility='onchange')
    sales_general_conditions = fields.Text("General Conditions", track_visibility='onchange')
    sales_authorize_different_address = fields.Boolean(
        "Authorize Different Addresses for Delivery and Invoicing", 
        track_visibility='onchange'
    )
    sales_modify_sale_order = fields.Text("Modify Sale Order", track_visibility='onchange')

    # comptabilite - Accounting Default Parameters
    accounting_last_day_fiscal_exercise = fields.Integer(
        string="Last Day of Fiscal Exercise",
        default=31,
        track_visibility='onchange'
    )
    accounting_last_month_fiscal_exercise = fields.Selection(
        get_accounting_last_month_fiscal_exercise_options, 
        default='12', 
        string="Last Month of Fiscal Exercise", 
        track_visibility='onchange'
    )
    accounting_currency = fields.Many2one(
        'res.currency', 
        string='Default company currency', 
        help="Main currency of the company.", 
        track_visibility='onchange'
    )
    accounting_analytic_acc = fields.Boolean("Analytic Accounting", track_visibility='onchange')
    accounting_asset_management = fields.Boolean("Assets Management", track_visibility='onchange')
    accounting_revenu_recognition = fields.Boolean("Revenue Recognition", track_visibility='onchange')
    accounting_budget_management = fields.Boolean("Budget Management", track_visibility='onchange')
    accounting_output_bvr = fields.Boolean("Output BVR", track_visibility='onchange')
    accounting_iso_payment = fields.Boolean("ISO20022 Payment", track_visibility='onchange')
    accounting_foreign_currencies_list = fields.Boolean("Foreign Currencies List", track_visibility='onchange')
    accounting_tax_update_frequence = fields.Selection(
        get_accounting_tax_update_frequence_options, 
        string="Tax Update Frequence", 
        track_visibility='onchange'
    )
    accounting_reminder_levels = fields.Boolean("Reminder levels", track_visibility='onchange')

    # gestion de stock - Stock Management Default Parameters
    stock_mng_units_mesure = fields.Selection(
        get_stock_mng_units_mesure_options, 
        string="Units of Measure", 
        help="""Allows you to select and maintain different units of measure for products.""", 
        track_visibility='onchange'
    )
    stock_mng_prod_variants = fields.Selection(
        get_stock_mng_prod_variants_options, 
        string="Product Variants", 
        help='Work with product variant allows you to define some variant of the same products, an ease the product management in the ecommerce for example', 
        track_visibility='onchange'
    )
    stock_mng_packing_methods = fields.Selection(
        get_stock_mng_packing_methods_options, 
        string="Packing Methods", 
        help="""Allows you to create and manage your packaging dimensions and types you want to be maintained in your system.""", 
        track_visibility='onchange'
    )
    stock_mng_dropshipping = fields.Selection(
        get_stock_mng_dropshipping_options, string="Dropshipping",
        help='\nCreates the dropship route and add more complex tests\n'
             '-This installs the module stock_dropshipping.',
             track_visibility='onchange')
    stock_mng_generate_journal_item = fields.Boolean(
        "Generate a journal item for every stock movement", 
        track_visibility='onchange'
    )
    stock_mng_product_owners = fields.Selection(
        get_stock_mng_product_owners_options, 
        string="Product Owners", 
        help="""This way you can receive products attributed to a certain owner. """, 
        track_visibility='onchange'
    )
    stock_mng_expiration_dates = fields.Selection(
        get_stock_mng_expiration_dates_options, string="Expiration Dates",
        help="""Track different dates on products and serial numbers.
                The following dates can be tracked:
                - end of life
                - best before date
                - removal date
                - alert date.
                This installs the module product_expiry.""",
                track_visibility='onchange')
    stock_mng_lots_serial_nb = fields.Selection(
        get_stock_mng_lots_serial_nb_options, string="Lots and Serial Numbers",
        help="""This allows you to assign a lot (or serial number) to the pickings and moves.  This can make it possible to know which production lot was sent to a certain client, ...""", 
        track_visibility='onchange'
    )
    # - END - #


    # incoming email server funtions
    @api.onchange('incoming_email_server_type', 'incoming_email_server_security')
    def onchange_incoming_email_server_type(self):
        self.incoming_email_server_port = 0
        if self.incoming_email_server_type == 'pop':
            self.incoming_email_server_port = self.incoming_email_server_security and 995 or 110
        elif self.incoming_email_server_type == 'imap':
            self.incoming_email_server_port = self.incoming_email_server_security and 993 or 143

    # outgoing email server functions
    @api.onchange('outgoing_email_server_security')
    def _onchange_outgoing_email_server_security(self):
        if self.outgoing_email_server_security == 'ssl':
            self.outgoing_email_server_port = 465
        else:
            self.outgoing_email_server_port = 25
