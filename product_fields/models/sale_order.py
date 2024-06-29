# -*- coding: utf-8 -*-
from odoo import api,fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_prime_customer = fields.Boolean(string='Is prime customer', readonly=True)
    partner_product_ids = fields.Many2many('product.template', compute='_compute_partner_product_ids', store=True,
                                           string='Partner product')

    @api.depends('partner_id')
    def _compute_partner_product_ids(self):
        for rec in self:
            rec.is_prime_customer = rec.partner_id.is_prime_customer
            if rec.is_prime_customer:
                rec.partner_product_ids = self.env['product.template'].search([('product_master_type', '=', 'branded')]).mapped(
               'id')
                rec.order_line.write({
                    'product_template_id': [fields.Command.link(record.id) for record in rec.partner_product_ids],

                })
            else:
                rec.partner_product_ids = self.env['product.template'].search([])