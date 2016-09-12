# -*- coding: utf-8 -*-
# © 2016 Coninckx David (Open Net Sarl)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, fields, api, _
from openerp.tools import append_content_to_html

class account_report_context_followup(models.TransientModel):
    _inherit = 'account.report.context.followup'

    @api.multi
    def send_email(self):
        email = self.env['res.partner'].browse(self.partner_id.address_get(['invoice'])['invoice']).email
        if email and email.strip():
            email = self.env['mail.mail'].create({
                'subject': _('%s Payment Reminder') % self.env.user.company_id.name,
                'body_html': append_content_to_html(self.with_context(public=True, mode='print').get_html(), self.env.user.signature, plaintext=False),
                'email_from': self.env.user.email or '',
                'email_to': email,
                'email_cc' : 'jae@open-net.ch',
            })
            msg = _(': Sent a followup email')
            self.partner_id.message_post(body=msg, subtype='account_reports.followup_logged_action')
            return True
        return False