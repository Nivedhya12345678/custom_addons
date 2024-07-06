# -*- coding: utf-8 -*-
from odoo import api, fields, models
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_ids = fields.Many2many('product.product', string="Multiple products")

    def set_values(self):
        """Set values from the class ResConfigSettings"""
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'bill_of_material_in_cart.product_ids', self.product_ids.ids)
        return res

    @api.model
    def get_values(self):
        """Get values from the class ResConfigSettings"""
        res = super(ResConfigSettings, self).get_values()
        with_user = self.env['ir.config_parameter'].sudo()
        multiple_products = with_user.get_param('bill_of_material_in_cart.product_ids')
        res.update(product_ids=[(6, 0, literal_eval(multiple_products))] if multiple_products else False, )
        return res
