# -*- coding: utf-8 -*-
from datetime import date
from odoo import fields, models, api, exceptions
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
import io
import json
import xlsxwriter


class FleetAuctionWizard(models.TransientModel):
    _name = 'fleet.auction.wizard'
    _description = 'Fleet auction report'

    from_date = fields.Date(string='From date')
    to_date = fields.Date(string='To date')
    state = fields.Selection(
                             selection=[('draft', 'Draft'),
                                        ('confirmed', 'Confirmed'),
                                        ('ongoing', 'Ongoing'),
                                        ('success', 'Success'),
                                        ('cancelled', 'Cancelled')])
    customer_id = fields.Many2one("res.partner", string="Customer")
    current_user = fields.Many2one('res.users', string='Responsible')

    def action_print(self):
        customer_id = self.customer_id.name
        responsible_id = self.current_user.id
        from_date = self.from_date
        to_date = self.to_date
        state = self.state
        print(state)

        data = {'customer': customer_id, 'responsible': responsible_id, 'from_date': from_date,
                'to_date': to_date, 'state': state}
        print(data)

        if self.from_date and self.to_date:
            if self.to_date < self.from_date:
                raise ValidationError('Sorry, To Date Must be greater Than From Date...')

        return self.env.ref('fleet_auction.action_report_fleet_template').report_action(None, data=data)

    def print_xlsx(self):
        print('xlsx')
        customer_id = self.customer_id.name
        responsible_id = self.current_user.id
        from_date = self.from_date
        to_date = self.to_date
        state = self.state

        data = {'customer': customer_id, 'responsible': responsible_id, 'from_date': from_date,
                'to_date': to_date, 'state': state}
        if from_date and to_date:
            if to_date < from_date:
                raise ValidationError('Sorry, To Date Must be greater Than From Date...')

        return {
            'type': 'ir.actions.report',
            'data': {'model': 'fleet.auction.wizard',
                     'options': json.dumps(data,
                                           default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        print(data)
        print('get xlsx')
        query ="""select  fv.name as vehicle, re.name, fl.start_date, fl.end_date, fl.customer_id ,
                   fl.state , fl.current_value, bi.state as bid_state, bi.bid_amount, fl.current_user,
                   fl.won_price from fleet_auction as fl
                   inner join res_partner as re on re.id = fl.customer_id
                   inner join res_users as ru on ru.id = fl.current_user
                   inner join bid_fleet as bi on bi.customer_id = fl.customer_id and bi.auction_id = fl.id
                   inner join fleet_vehicle as fv on fv.id = fl.vehicle_name_id where 1=1 """

        if data['customer']:
            query += f" and re.name = '{data['customer']}'"
        if data['responsible']:
            query += f" and ru.id= {data['responsible']}"
        if data['from_date']:
            query += f" and fl.start_date >= '{data['from_date']}'"
        if data['to_date']:
            query += f" and fl.end_date <= '{data['to_date']}'"
        if data['state']:
            query += f" and fl.state = '{data['state']}'"

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        print(report)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '15px'})
        format1 = workbook.add_format({'font_size': 10, 'align': 'center'})

        cell_text_format = workbook.add_format({'bold': True, 'font_size': 9, 'align': 'center'})

        sheet.merge_range('B2:D3', 'FLEET AUCTION REPORT', head)
        sheet.set_column('A:B', 18)
        sheet.set_column('D:F', 18)
        sheet.set_column('I:J', 18)
        sheet.set_column('C:C', 18)
        sheet.set_column('H:H', 18)
        sheet.set_column('G:G', 18)

        if data['customer']:
            sheet.write('A4', 'Customer Name')
            sheet.write('B4', data['customer'])
            sheet.set_column('C:C', None, None, {"hidden": True})
        if data['state']:
            sheet.write('A6', 'State')
            sheet.write('B6', dict(self.env['fleet.auction']._fields['state'].selection).get(data['state']))
            sheet.set_column('H:H', None, None, {"hidden": True})
        if data['responsible']:
            sheet.write('A5', 'Responsible')
            sheet.write('B5', self.env['res.users'].browse(data['responsible']).name)
            sheet.set_column('G:G', None, None, {"hidden": True})

        sheet.write('A7', 'Sl.No', cell_text_format)
        sheet.write('B7', 'Fleet Name', cell_text_format)
        if not data['customer']:
            sheet.write('C7', 'Customer Name', cell_text_format)
        sheet.write('D7', 'From date', cell_text_format)
        sheet.write('E7', 'To date', cell_text_format)
        sheet.write('F7', 'Current asset value', cell_text_format)
        sheet.write('G7', 'Responsible', cell_text_format)
        if not data['state']:
            sheet.write('H7', 'State', cell_text_format)
        sheet.write('I7', 'Bid amount', cell_text_format)
        sheet.write('J7', 'Won price', cell_text_format)
        sheet.write('E1', 'Print date')
        sheet.write('F1', str(date.today()))

        row = 7
        number = 1
        for line in report:
            sheet.write(row, 0, number, format1)
            sheet.write(row, 1, line['vehicle'], format1)
            if not data['customer']:
                sheet.write(row, 2, line['name'], format1)
            sheet.write(row, 3, str(line['start_date']), format1)
            sheet.write(row, 4, str(line['end_date']), format1)
            sheet.write(row, 5, line['current_value'], format1)
            if not data['responsible']:
                sheet.write(row, 6, self.env['res.users'].browse(line['current_user']).name, format1)
            if not data['state']:
                sheet.write(row, 7, dict(self.env['fleet.auction']._fields['state'].selection).get(line['state']),
                            format1)
            sheet.write(row, 8, line['bid_amount'], format1)
            sheet.write(row, 9, line['won_price'], format1)
            row += 1
            number += 1

        sheet.write('E3:E3', self.env.company.name)
        sheet.write('E4:E4', self.env.company.email)
        sheet.write('E5:E5', self.env.company.phone)

        workbook.close()
        output.seek(0)
        if report:
            response.stream.write(output.read())
        else:
            raise exceptions.UserError('There is no data to generate reports')

        output.close()



