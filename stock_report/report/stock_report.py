# -*- coding: utf-8 -*-
from odoo import models, api


class StockReport(models.AbstractModel):
    _name = 'report.stock_report.product_stock_report'

    @api.model
    def _get_report_values(self,  docids, data=None):
        query = """select st.product_id ,st.quantity, pt.list_price, pt.name ->> 'en_US' as product, 
                       st.location_id, pt.default_code,stl.complete_name from stock_quant as st 
                       inner join product_product as pr on pr.id = st.product_id
                       inner join product_template as pt on pt.id = pr.product_tmpl_id
                       inner join stock_location as stl on stl.id = st.location_id 
                       order by st.location_id desc"""

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = self.env['stock.location'].sudo().browse(list(set([i['location_id'] for i in report])))
        return {
            'docs': report,
            'data': data,
        }
