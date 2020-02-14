import { set, get } from "~/utils";
const state = () => ({
  shipping: null,
  billing: null,
  stripeToken: ""
});
const getters = {
  shipping: get("shipping"),
  billing: get("billing"),
  stripeToken: get("stripeToken")
};
const actions = {
  clear({ commit }) {
    commit("setShipping", null);
    commit("setBilling", null);
    commit("setStripeToken", null);
  },
  initData({ commit, dispatch }) {
    dispatch("profile/fetchAddresses", null, { root: true }).then(data => {
      let default_shipping = data.find(
        i => i.default && i.address_type === "S"
      );
      let default_billing = data.find(i => i.default && i.address_type === "B");
      commit("setShipping", default_shipping);
      commit("setBilling", default_billing);
    });
  }
};
const mutations = {
  setShipping: set("shipping"),
  setBilling: set("billing"),
  setStripeToken: set("stripeToken")
};

export default {
  state,
  getters,
  actions,
  mutations
};
