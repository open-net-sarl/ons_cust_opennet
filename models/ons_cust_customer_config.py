# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

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

class OnsCustCustomerConfig(models.Model):
    _name = "ons.cust.customer.config"

    @api.model
    def get_selection_language(self):
        _logger.info("INSIDE")
        info_vals = self.env['res.lang'].sudo().search([('id', '!=', '0')])
        _logger.info(info_vals)
        return [(lang.code, lang.name) for lang in info_vals]

    user_id = fields.Many2one(
        'res.users', 
        string='Customer', 
        required=True,
        readonly=True)

    # - Votre Société - #
    # company info
    logo = fields.Binary('Logo (vectorial)', attachment=True)
    email = fields.Char("Administrator's Email")

    # bank info
    bank_account_type = fields.Selection(
        [('bank', 'Bank'), ('iban', 'IBAN')],
        string='Bank Account Type')
    iban = fields.Char('IBAN')
    bank_account_number = fields.Char('Bank Account Number')
    bvr_number = fields.Char('BVR Number')
    bank_name = fields.Char('Bank Name')
    # - END - #

    # - Configurations - #
    # serveur d'email entrant - Incoming Email Server
    incoming_email_server_type = fields.Selection([
        ('pop', 'POP Server'),
        ('imap', 'IMAP Server'),
    ],"Server's Type", default='pop')
    incoming_email_server_name = fields.Char("Server's Name", help="Hostname or IP of the mail server")
    incoming_email_server_port = fields.Char("Port")
    incoming_email_server_security = fields.Boolean("Security SSL/TLS", help="Connections are encrypted with SSL/TLS through a dedicated port (default: IMAPS=993, POP3S=995)")
    incoming_email_server_username = fields.Char("Username")
    incoming_email_server_pass = fields.Char("Password")

    # serveur d'email sortant - Outgoing Email Server
    outgoing_email_server_name = fields.Char("SMTP Server", help="Hostname or IP of SMTP server")
    outgoing_email_server_port = fields.Char("SMTP Port", default=25, help="SMTP Port. Usually 465 for SSL, and 25 or 587 for other cases.")
    outgoing_email_server_security = fields.Selection(
        [('none', 'None'),
        ('starttls', 'TLS (STARTTLS)'),
        ('ssl', 'SSL/TLS')],
        default='none',
        string="Security", 
        help="Choose the connection encryption scheme:\n"
            "- None: SMTP sessions are done in cleartext.\n"
            "- TLS (STARTTLS): TLS encryption is requested at start of SMTP session (Recommended)\n"
            "- SSL/TLS: SMTP sessions are encrypted with SSL/TLS through a dedicated port (default: 465)")
    outgoing_email_server_username = fields.Char("Username", help="Optional username for SMTP authentication")
    outgoing_email_server_password = fields.Char("Password", help="Optional username for SMTP authentication")

    # numerotation de vos documents - Document Numbering
    doc_numb_quot_sales = fields.Char("Quotations & Sales")
    doc_numb_invoices = fields.Char("Invoices")
    doc_numb_purchases = fields.Char("Purchase Orders")
    doc_numb_delivery = fields.Char("Delivery Orders")

    # carnet d'adress - Contact Default Parameter
    contacts_lang = fields.Selection(
        get_selection_language,
        string="Language")
    contacts_payment_terms = fields.Many2one(
        'account.payment.term',
        string='Payment Terms',
        help="This payment term will be used instead of the default one for sale orders and customer invoices")
    contacts_products_type = fields.Char("Product's Type")

    # articles - Product Default Parameters
    products_can_be_sold = fields.Boolean("Can Be Sold")
    products_can_be_bought = fields.Boolean("Can Be Bought")
    products_warranty = fields.Integer("Warranty (months)")
    products_delivery_delay = fields.Integer("Delivery Delay to the Customer (days)")
    products_earnings_acc = fields.Char("Earnings Account")
    products_spendings_acc = fields.Char("Spendings Account")
    products_customer_tax = fields.Many2one('account.tax', string="Customer Tax", domain=[('type_tax_use', '=', 'sale')])
    products_supplier_tax = fields.Many2one('account.tax', string="Supplier Tax", domain=[('type_tax_use', '=', 'purchase')])
    products_supply_routes = fields.Char("Supply Routes")
    products_unit_of_mesure = fields.Many2one('product.uom', string="Unit of Mesure")

    # ventes - Sales Parameters
    sales_sale_price = fields.Selection(
        [('fixed', 'A single sale price per product'),
        ('percentage', 'Specific prices per customer segment, currency, etc.'),
        ('formula', 'Advanced pricing based on formulas (discounts, margins, rounding)')], 
        default='fixed',
        string="Sale's Price",
        help='Fix Price: all price manage from products sale price.\n'
             'Different prices per Customer: you can assign price on buying of minimum quantity in products sale tab.\n'
             'Advanced pricing based on formula: You can have all the rights on pricelist')
    sales_invoicing_policy = fields.Char("Invoicing Policy")
    sales_general_conditions = fields.Text("General Conditions")
    sales_autorize_different_address = fields.Boolean("Autorize Different Addresses for Delivery and Invoicing")
    sales_modify_sale_order = fields.Text("Modify Sale Order")

    # comptabilite - Accounting Default Parameters
    accounting_last_day_fiscal_exercise = fields.Integer(
        string="Last Day of Fiscal Exercise", 
        default=31)
    accounting_last_month_fiscal_exercise = fields.Selection(
        [(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), 
        (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], 
        default=12,
        string="Last Month of Fiscal Exercise")
    accounting_currency = fields.Many2one(
        'res.currency',
        string='Default company currency', 
        help="Main currency of the company.")
    accounting_analytic_acc = fields.Boolean("Analytic Account")
    accounting_asset_management = fields.Boolean("Asset's Management")
    accounting_recognize_earnings = fields.Boolean("Recognize Ernings")
    accounting_budget_management = fields.Boolean("Budget Management")
    accounting_output_bvr = fields.Boolean("Output BVR")
    accounting_iso_payment = fields.Boolean("ISO20022 Payment")
    accounting_foreign_currencies_list = fields.Boolean("Foreign Currencies List")
    accounting_tax_update_frequence = fields.Selection(
        [('manually','Manually'),('daily','Daily'),('weekly','Weekly'),('monthly','Monthly')],
        string="Tax Update Frequence")
    accounting_reminder_levels = fields.Boolean("Reminder levels")

    # gestion de stock - Stock Management Default Parameters
    stock_mng_units_mesure = fields.Selection(
        [(0, 'Products have only one unit of measure (easier)'),
        (1, 'Some products may be sold/purchased in different units of measure (advanced)')],
        string="Units of Measure",
        help="""Allows you to select and maintain different units of measure for products.""")
    stock_mng_prod_variants = fields.Selection(
        [(0, "No variants on products"),
        (1, 'Products can have several attributes, defining variants (Example: size, color,...)')], 
        string="Product Variants",
        help='Work with product variant allows you to define some variant of the same products, an ease the product management in the ecommerce for example')
    stock_mng_packing_methods = fields.Selection(
        [(0, 'Do not manage packaging'),
        (1, 'Manage available packaging options per products')], 
        string="Packing Methods",
        help="""Allows you to create and manage your packaging dimensions and types you want to be maintained in your system.""")
    stock_mng_dropshipping = fields.Selection(
        [(0, 'Suppliers always deliver to your warehouse(s)'),
        (1, "Allow suppliers to deliver directly to your customers")],
        string="Dropshipping",
        help='\nCreates the dropship route and add more complex tests\n'
             '-This installs the module stock_dropshipping.')
    stock_mng_generate_journal_item = fields.Boolean("Generate a journal item for every stock movement")
    stock_mng_product_owners = fields.Selection(
        [(0, 'All products in your warehouse belong to your company'),
        (1, 'Manage consignee stocks (advanced)')], 
        string="Product Owners",
        help="""This way you can receive products attributed to a certain owner. """)
    stock_mng_expiration_dates = fields.Selection(
        [(0, 'Do not use Expiration Date on serial numbers'),
        (1, 'Define Expiration Date on serial numbers')], 
        string="Expiration Dates",
        help="""Track different dates on products and serial numbers.
                The following dates can be tracked:
                - end of life
                - best before date
                - removal date
                - alert date.
                This installs the module product_expiry.""")
    stock_mng_lots_serial_nb = fields.Selection(
        [(0, 'Do not track individual product items'),
        (1, 'Track lots or serial numbers')], 
        string="Lots and Serial Numbers",
        help="""This allows you to assign a lot (or serial number) to the pickings and moves.  This can make it possible to know which production lot was sent to a certain client, ...""")
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
