# -*- coding: utf-8 -*-
from odoo import models


class PosSession(models.Model):

    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        """Loading field"""
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('owner_id')
        return result
