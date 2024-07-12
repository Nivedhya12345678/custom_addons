/** @odoo-module */

import { Orderline } from "@point_of_sale/app/generic_components/orderline/orderline";
import { patch } from "@web/core/utils/patch";

patch(Orderline.prototype, {
    removeLine() {
        const order = this.env.services.pos.get_order();
        const orderline = order.orderlines.find((line) => line.id);
        return order.removeOrderline(orderline);
    }
});





