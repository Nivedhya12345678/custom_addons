# -*- coding: utf-8 -*-
from odoo import fields, models


class RevenueWiseCommission(models.Model):
    _name = "revenue.commission"
    _description = "Revenue wise commission"

    commission_id = fields.Many2one('crm.commission', string='Commission plan')
    sequence = fields.Integer(string='Sequence')
    from_amount = fields.Float(string='From amount')
    to_amount = fields.Float(string='To amount')
    # revenue_type = fields.Selection(selection=[('straight','Straight'), ('graduated', 'Graduated')])
    rate = fields.Float(string='Rate(%)')

