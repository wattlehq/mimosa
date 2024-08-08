import { OrderFindParcel } from "./core/orderFindParcel.js";
import { OrderForm } from "./core/orderForm.js";

document.addEventListener('DOMContentLoaded', () => {
  const inputSelectionTarget = '.order-form input[name="property_id"]';
  new OrderFindParcel(inputSelectionTarget);
  new OrderForm();
});
