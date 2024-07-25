# -*- coding: utf-8 -*-
from odoo import _, fields, models, service

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('paytrail', "Paytrail")], ondelete={'paytrail': 'set default'})
    paytrail_merchant_id = fields.Char(
        string="Merchant Id",
        required_if_provider='paytrail',
    )
    paytrail_secret_key = fields.Char(
        string="Paytrail Secret key",
        required_if_provider='paytrail',
        groups='base.group_system',
    )

