export default function({ store, redirect }) {
  if (!store.getters["cart/getCart"] || !store.getters["cart/cartCount"]) {
    return redirect({ name: "cart" });
  }
}
