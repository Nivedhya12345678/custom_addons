# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_order_ids = fields.One2many('sale.order', inverse_name='partner_id', string='Sale order')
    product_count = fields.Integer(compute='_product_count',string="Product Count")

    def action_total_product(self):
        print(self.sale_order_ids.order_line.product_id.ids)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.sale_order_ids.order_line.product_id.ids)],
            'context': "{'create': False}"
        }

    def _product_count(self):
        """ calculating the product count"""
        for record in self:
            record.product_count = self.env['sale.order'].search_count(
                [('state', '=', 'sale'), ('partner_id', '=', self.id)])
