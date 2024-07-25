# -*- coding: utf-8 -*-
import base64

from odoo import models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def scheduled_action(self):
        report_template_id = self.env.ref(
            'stock_report.action_report_stock_template')

        data_record = base64.b64encode(self.env['ir.actions.report'].sudo()._render_qweb_pdf(report_template_id,
                                                                                             [self.id], data=None)[0])
        ir_values = {
            'name': 'Stock Report',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/pdf',
        }

        stock_report_attachment_id = self.env[
            'ir.attachment'].sudo().create(ir_values)

        if stock_report_attachment_id:
            email_template = self.env.ref(
                'stock_report.mail_template_stock_report')

        manager_email = self.env['res.users'].search([('groups_id.name', '=', 'Administrator'),
                                                    ('groups_id.category_id.name', '=', 'Inventory')]).email
        if manager_email:
            email = manager_email

        if email_template and email:
            email_values = {
                'email_to': email,
            }

            email_template.attachment_ids = [
                (4, stock_report_attachment_id.id)]

            email_template.send_mail(
                self.id, email_values=email_values, force_send=True)
            email_template.attachment_ids = [(5, 0, 0)]