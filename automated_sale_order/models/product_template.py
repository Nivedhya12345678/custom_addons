from odoo import models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_open_quotations(self):
        # print(self.list_price)
        # print(self.seller_ids.price)
        # print(self.product_variant_id.name)
        # print(self.seller_ids[0].partner_id.name)
        # print(self.seller_ids[0].price)

        return {
            'name': 'Add Details',
            'type': 'ir.actions.act_window',
            'res_model': 'product.template.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'context': {'default_partner_id': self.seller_ids[0].partner_id.id, 'default_price_unit': self.seller_ids[0].price ,
                        'default_product_id': self.product_variant_id.id},
            'target': 'new'
        }
