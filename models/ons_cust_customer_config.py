# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api

class OnsCustCustomerConfig(models.Model):
    _name = "ons.cust.customer.config"

    user_id = fields.Many2one('res.users', string='Customer', required=True)

    # - Votre Société - #
    # company info
    logo = fields.Binary('Logo (vectorial)')
    email = fields.Char("Administrator's Email")
    # bank info
    bank_account_type = fields.Char('Bank Account Type')
    iban = fields.Char('IBAN')
    bank_account_number = fields.Char('Bank Account Number')
    bvr_number = fields.Char('BVR Number')
    bank_name = fields.Char('Bank Name')

    # - Configurations - #
    # serveur d'email entrant - Incoming Email Server
    incoming_email_server_type = fields.Char("Server's Type")
    incoming_email_server_name = fields.Char("Server's Name")
    incoming_email_server_port = fields.Char("Port")
    incoming_email_server_security = fields.Char("Security SSL/TLS")
    incoming_email_server_username = fields.Char("Username")
    incoming_email_server_pass = fields.Char("Password")
    # serveur d'email sortant - Outgoing Email Server
    outgoing_email_server_name = fields.Char("SMTP Server")
    outgoing_email_server_port = fields.Char("SMTP Port")
    outgoing_email_server_security = fields.Char("Security")
    outgoing_email_server_username = fields.Char("Username")
    outgoing_email_server_password = fields.Char("Password")
    # numerotation de vos documents - Document Numbering
    doc_numb_quot_sales = fields.Char("Quotations & Sales")
    doc_numb_invoices = fields.Char("Invoices")
    doc_numb_purchases = fields.Char("Purchase Orders")
    doc_numb_delivery = fields.Char("Delivery Orders")
    # carnet d'adress - Contact Default Parameter
    contacts_lang = fields.Char("Language")
    contacts_payment_condition = fields.Char("Payment Condition")
    contacts_products_type = fields.Char("Product's Type")
    # articles - Product Default Parameters
    products_can_be_sold = fields.Char("Can Be Sold")
    products_can_be_bought = fields.Char("Can Be Bought")
    products_warranty = fields.Char("Warranty (months)")
    products_delivery_delay = fields.Char("Delivery Delay to the Customer (days)")
    products_earnings_acc = fields.Char("Earnings Account")
    products_spendings_acc = fields.Char("Spendings Account")
    products_sale_tax = fields.Char("Sale Tax")
    products_purchase_tax = fields.Char("Purchase Tax")
    products_supply_routes = fields.Char("Supply Routes")
    products_mesure_units = fields.Char("Mesure Units")
    # ventes - Sales Parameters
    sales_sale_price = fields.Char("Sale's Price")
    sales_invoicing_policy = fields.Char("Invoicing Policy")
    sales_general_conditions = fields.Char("General Conditions")
    sales_autorize_different_address = fields.Char("Autorize Different Addresses for Delivery and Invoicing")
    sales_modify_sale_order = fields.Char("Modify Sale Order")
    # comptabilite - Accounting Default Parameters
    accounting_last_day_fiscal_exercise = fields.Char("Last Day of Fiscal Exercise")
    accounting_currency = fields.Char("Currency")
    accounting_analytic_acc = fields.Char("Analytic Account")
    accounting_asset_management = fields.Char("Asset's Management")
    accounting_recognize_earnings = fields.Char("Recognize Ernings")
    accounting_budget_management = fields.Char("Budget Management")
    accounting_output_bvr = fields.Char("Output BVR")
    accounting_iso_payment = fields.Char("ISO20022 Payment")
    accounting_foreign_currencies_list = fields.Char("Foreign Currencies List")
    accounting_tax_update_frequence = fields.Char("Tax Update Frequence")
    accounting_reminder_levels = fields.Char("Reminde's levels")
    # gestion de stock