import { FindParcel } from "./core/findParcel.js";
import { OrderForm } from "./core/orderForm.js";

document.addEventListener('DOMContentLoaded', () => {
  const inputSelectionTarget = '.order-form input[name="property_id"]';
  new FindParcel(inputSelectionTarget);
  new OrderForm();
});
