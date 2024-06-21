from odoo import fields, models


class FleetCancelWizard(models.TransientModel):
    _name = 'fleet.cancel.wizard'
    _description = 'Get cancel Reason'

    cancel_reason_id = fields.Many2one('fleet.cancel.reason', 'Cancel Reason')
    cancel_id = fields.Many2one('fleet.auction', string='Cancel')

    def action_cancel_reason(self):
        res = self.cancel_id.write({'state': 'cancelled'})
        return res
