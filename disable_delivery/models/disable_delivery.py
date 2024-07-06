# -*- coding: utf-8 -*-
from odoo import api,fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    delivery_count = fields.Integer(string='Delivery')

    def action_confirm(self):

        return super().action_confirm()

    def action_delivery(self):
        return self._get_action_view_picking(self.picking_ids)



