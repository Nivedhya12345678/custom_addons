# -*- coding: utf-8 -*-
from odoo import fields, models,api


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    total_sale_order = fields.Float(compute='_compute_sale_order', string='Total sale order')

    @api.depends('default_code')
    def _compute_sale_order(self):
        for record in self:
            record.total_sale_order = self.env['sale.order.line'].search_count(
                [('product_id', '=', self.id)])
            print(record.total_sale_order)