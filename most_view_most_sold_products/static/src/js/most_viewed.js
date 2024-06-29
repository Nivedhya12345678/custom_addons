/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import { renderToFragment } from "@web/core/utils/render";

export function chunk(array, size) {
    const result = [];
    for (let i = 0; i < array.length; i += size) {
        result.push(array.slice(i, i + size));
    }
    return result;
}

var MostViewedProducts = PublicWidget.Widget.extend({

        selector: '.top_viewed_product_snippet',
        willStart: async function () {
            const data = await jsonrpc('/most_viewed_products', {})
            console.log('data',data)
            Object.assign(this, {
                data
            })

        },
        start: function () {
        const refEl = this.$el.find("#top_viewed_products")
        var chunks = chunk(this.data, 4)
        chunks[0].is_active = true
        var unique_id = Date.now()
        refEl.html(renderToFragment('most_view_most_sold_products.most_viewed_products',{
          'products':chunks,
          'unique_id':unique_id,
        }))

        },
  });
    PublicWidget.registry.top_viewed_product_snippet =  MostViewedProducts;
    return MostViewedProducts;


