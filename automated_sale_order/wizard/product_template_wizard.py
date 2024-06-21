from odoo import Command, fields, models


class ProductTemplateWizard(models.TransientModel):
    _name = 'product.template.wizard'
    _description = 'Details'

    partner_id = fields.Many2one('res.partner', string='Customer')
    product_qty = fields.Float(string="Quantity", default=1.0)
    price_unit = fields.Float(string='Price')
    product_id = fields.Many2one('product.product', string='Product', readonly=True)

    def action_confirm_wizard(self):
        """Check if there is an open quotation for customer"""
        # print(self.product_id.seller_ids.partner_id.name)
        quotation = self.env['sale.order'].search([('partner_id', '=', self.partner_id.id),
                                                   ('state', '=', 'draft'),], limit=1)
        if quotation:
            quotation.write({
                'order_line': [Command.create({
                    'product_id': self.product_id.id,
                    'product_uom_qty': self.product_qty,
                    'price_unit': self.price_unit,
                })]
            })
        else:
            """Creating new quotation"""
            # for rec in self:
            quotation = self.env['sale.order'].create([{
                'partner_id': self.partner_id.id,
                'date_order': fields.Date.context_today(self),
                'order_line': [Command.create({
                    'product_id': self.product_id.id,
                    'product_uom_qty': self.product_qty,
                    'price_unit': self.price_unit,
                })]
            }])
        quotation.action_confirm()
        return {
                'type': 'ir.actions.act_window',
                'res_model': 'sale.order',
                'view_type': 'form',
                'view_mode': 'form',
                'res_id': quotation.id,
                'target': 'current'
        }
