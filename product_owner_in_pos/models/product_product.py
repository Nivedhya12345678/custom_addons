# -*- coding: utf-8 -*-
from odoo import fields,models


class ProductTemplate(models.Model):
    _inherit = 'product.product'

    owner_id = fields.Many2one('res.partner', string="Product owner")
