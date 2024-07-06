# -*- coding: utf-8 -*-
import ast
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class WebsiteSaleInherit(WebsiteSale):
    @http.route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, **post):
        response = super(WebsiteSaleInherit, self).cart(**post)

        """ Fetch BoM details for selected products"""
        bom_details = []
        product_ids = ast.literal_eval(
            request.env['ir.config_parameter'].sudo().get_param('bill_of_material_in_cart.product_ids'))
        product = request.env['product.product'].browse(product_ids)
        for rec in product:
            for bom_line in rec.bom_ids.bom_line_ids:
                bom_details.append({
                    'product_name': bom_line.product_id.name,
                    'default_code': bom_line.product_id.default_code,
                    'product_id': rec,
                })
        response.qcontext.update({
            'bom_details': bom_details,
        })
        return response
