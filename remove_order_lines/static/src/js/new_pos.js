/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { Order } from "@point_of_sale/app/store/models";

patch(Order.prototype, {
    async pay(){
    console.log("loard")
    var order = this.get_orderlines();
    var sum = 0
    order.forEach(line =>{
    sum +=line.price

    console.log(sum)
    });

    console.log(order)
    super.pay(...arguments);


    }
});