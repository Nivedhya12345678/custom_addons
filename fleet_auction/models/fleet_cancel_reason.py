from odoo import fields, models


class CancelReason(models.Model):
    _name = "fleet.cancel.reason"
    _description = 'Fleet Cancel Reason'

    name = fields.Char('Description', required=True)
