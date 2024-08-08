import { FindParcel } from "./findParcel.js";
import { OrderForm } from "./orderForm.js";

document.addEventListener('DOMContentLoaded', () => {
  const inputSelectionTarget = '.order-form input[name="property_id"]';
  new FindParcel(inputSelectionTarget);
  new OrderForm();
});
