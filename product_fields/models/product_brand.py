# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductBrand(models.Model):
    _name = "product.brand"
    _description = 'Product Brand'
    _rec_name = "brand"

    brand = fields.Char(string='Product Brand')
