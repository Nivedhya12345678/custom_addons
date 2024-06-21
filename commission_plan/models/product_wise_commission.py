# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductWiseCommission(models.Model):
    _name = "product.commission"
    _description = "Product wise commission"

    commission_id = fields.Many2one('crm.commission', string='Commission plan')
    product_id = fields.Many2one('product.product', string='Product')
    product_category_id = fields.Many2one('product.category', string='Product category')
    maximum_amount = fields.Float(string='Commission Amount')
    rate_percentage = fields.Float(string='Rate(%)')

