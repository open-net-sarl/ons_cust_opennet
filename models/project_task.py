# -*- coding: utf-8 -*-
# © 2017 Open Net Sarl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import datetime
import logging

_logger = logging.getLogger(__name__)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def _cron_info_deadline_project_task(self):
        jae = self.env['res.users'].search([('login', '=', 'jae')], limit=1)
        tasks = self.search([])
        filtered_tasks = []
        for task in tasks:
            if task.stage_id.name == 'Open' or task.stage_id.name == 'En cours':
                filtered_tasks.append(task)
        for task in filtered_tasks:
            deadline = fields.Date.from_string(task.date_deadline)
            if deadline and deadline < datetime.datetime.today().date():
                if task.user_id:
                    mail = self.env.ref('ons_cust_opennet.info_deadline_project_task_cron')
                    mail.send_mail(task.id)
                else:
                    task.user_id = jae
                    mail = self.env.ref('ons_cust_opennet.info_deadline_project_task_cron')
                    mail.send_mail(task.id)

    @api.multi
    def info_for_deadline_project_task(self):
        action = self.env.ref('project.action_view_task') or False
        menu = self.env.ref('project.menu_action_view_task') or False
        return {'action': action,'menu': menu}
