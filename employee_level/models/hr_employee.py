# -*- coding: utf-8 -*-
from odoo import fields, models


class HrEmployeePrivate(models.Model):
    _inherit = 'hr.employee'

    employee_level_id = fields.Many2one('employee.level', string='Employee level')
    employee_salary = fields.Float(string='Salary')
    active_level = fields.Boolean(string='active')


    def action_promote(self):
        levels = self.employee_level_id.search_read([])
        print(levels)
        for rec in levels:
            if self.employee_level_id.id == rec['id']:
                print(rec['id'] + 1)
                self.employee_level_id = rec['id'] + 1
                self.employee_salary = rec['salary']
                print('hi')
                break







                # self.write({'employee_level_id': value})
            #     print(rec)
            #     print(self.employee_level_id)
            #     self.write({'employee_level_id': value})

