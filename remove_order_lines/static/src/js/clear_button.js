/** @odoo-module */

import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { _t } from "@web/core/l10n/translation";
import { Component } from "@odoo/owl";

export class ClearButton extends Component {
      static template = "point_of_sale.ClearButton";
      async removeLine() {
          const { confirmed } = await this.env.services.popup.add(ConfirmPopup, {
                 title: _t("Clear all orderlines"),
                 body: _t("Are you sure to clear this orders ?"),

          });
          if (!confirmed) {
          return false;
          }
          const order = this.env.services.pos.get_order();
          const orderline = order.orderlines;
          while(orderline.length > 0){
              orderline.forEach((line)=>{
                 order.removeOrderline(line)
              });
          }
      }
}
ProductScreen.addControlButton({
    component: ClearButton,
});


