# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand', string='Product Brand', required=True)
    product_master_type = fields.Selection(selection=[
        ('single', 'Single product'),
        ('branded', 'Branded product')], default='single', string='Product master type')
