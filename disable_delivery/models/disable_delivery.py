# -*- coding: utf-8 -*-
from odoo import api, fields, models, Command


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    allow_delivery = fields.Boolean(string='Allow delivery')

    def action_confirm(self):
        for order in self:
            if order.allow_delivery:
                order.allow_delivery == True
                self.order_line._action_launch_stock_rule()
            else:
                return super().action_confirm()

    def action_delivery(self):
        self.order_line._action_launch_stock_rule()
        return super().action_confirm()
       

