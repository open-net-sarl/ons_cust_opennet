# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# access_portal_project_task,portal_project_task,project.model_project_task,base.group_portal,1,0,0,0

{
    'name': 'Open-Net Customization for Open Net',
    'summary': 'Open Net Customization for Open Net',
    'description': 'Open Net Customization for Open Net',
    'category': 'Open Net customizations',
    'author': "Open Net Sàrl",
    'depends': [
        'account',
        'sale',
        'report',
        'ons_productivity_project_issue',
        'account_reports',
        'website_portal_sale',
        'event_barcode',
        'eagle_project',
        'stock',
        'project_issue'
    ],
    'version': '10.0.1.0.2',
    'auto_install': False,
    'website': 'http://open-net.ch',
    'license': 'AGPL-3',
    'images': [],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/ons_cust_crons.xml',
        'data/mail_template.xml',
        'views/project_task_views.xml',
        'views/ons_cust_opennet.xml',
        'views/eagle_views.xml',
        'views/stock_move_views.xml',
        'views/res_partner_views.xml',
        'views/report_external_header.xml',
        'views/report_external_footer.xml',
        'views/report_invoice.xml',
        'views/report_event_badge_templates.xml',
        # 'views/report_financial.xml',
        'views/ons_cust_customer_config_views.xml',
        'views/ons_cust_customer_changes_views.xml',
        'views/ons_cust_custumer_config_web_views.xml',
        'views/website_portal_templates.xml',
        'views/website_portal_sale_templates.xml',
        'report/account_followup_report_views.xml',
        'views/ons_functionnal_area_view.xml',
        'views/ons_pricing_template.xml',
        'views/ons_pricing_option_view.xml',
        'views/ons_hosting_view.xml',
        'views/ons_area_dependencies.xml'
    ],
    'installable': True
}
