# -*- coding: utf-8 -*-
from odoo import api,fields, models


class ResPartner(models.Model):
    _inherit = 'res.users'

    commission_id = fields.Many2one('crm.commission', string='Commission plan')
    sale_order_ids = fields.One2many('sale.order', inverse_name='user_id', string='Sale order',
                                     domain=[('commission_amount', '!=', 0)])

    total_commission = fields.Float(string='Total commission')


