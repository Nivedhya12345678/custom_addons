# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    brand_id = fields.Many2one('product.brand', string='Product brand')

    @api.onchange('product_id')
    def _change_brand_id(self):
        self.brand_id = self.product_id.brand_id
