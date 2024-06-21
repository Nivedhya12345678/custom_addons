from odoo import fields, models, api


class FleetBid(models.Model):
    _name = "employee.level"
    _description = "Employee Level"
    _rec_name = 'level'

    level = fields.Char(string='level ')

    salary = fields.Float(string='salary')
