# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

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
        'website_portal',
    ],
    'version': '10.0.1.0.2',
    'auto_install': False,
    'website': 'http://open-net.ch',
    'license': 'AGPL-3',
    'images': [],
    'data': [
        'security/ir.model.access.csv',
        'data/ons_cust_crons.xml',
        'views/project_task_views.xml',
        'views/ons_cust_opennet.xml',
        'views/report_external_header.xml',
        'views/report_external_footer.xml',
        'views/report_invoice.xml',
        # 'views/report_financial.xml',
        'views/ons_cust_customer_config_views.xml',
        'views/ons_cust_custumer_config_web_views.xml',
        'report/account_followup_report_views.xml',
    ],
    'installable': True
}
