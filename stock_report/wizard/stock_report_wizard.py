# -*- coding: utf-8 -*-
from datetime import date

from odoo import fields, models


class StockReportWizard(models.TransientModel):
    _name = 'stock.report.wizard'
    _description = 'Stock report'


    current_date = fields.Date(string='Cuurent date', default=date.today().strftime('%Y-%m-%d'))

    def action_print(self):
        date = self.current_date
        data = {'date': date}
        print(date)
        return self.env.ref('stock_report.action_report_stock_template').report_action(None, data=data)
