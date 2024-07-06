/** @odoo-module */
import { Orderline } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";


patch(Orderline.prototype, {
    getDisplayData() {
    console.log(this.get_product().owner_id)
        return {
            ...super.getDisplayData(...arguments),
            owner_id: this.get_product().owner_id,
        };
    },
});