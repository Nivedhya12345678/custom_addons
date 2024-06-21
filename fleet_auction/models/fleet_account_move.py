from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    fleet_id = fields.Many2one('fleet.auction', string="Fleet Number")

    def action_post(self):
        super(AccountMove, self).action_post()
        mail_template = self.env.ref('fleet_auction.mail_template')
        mail_template.send_mail(self.id, force_send=True)
        return
