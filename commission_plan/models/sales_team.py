# -*- coding: utf-8 -*-
from odoo import fields, models


class Team(models.Model):
    _inherit = 'crm.team'

    commission_id = fields.Many2one('crm.commission', string='Commission plan')
    sale_order_ids = fields.One2many('sale.order', inverse_name='team_id',
                                     domain=[('commission_amount', '!=', 0)])
    total_commission = fields.Float(string='Total commission')
