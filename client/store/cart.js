import { set, get } from "~/utils";
const state = () => ({
  cart: null,
  loading: 0
});
const getters = {
  getCart: get("cart"),
  getLoading: get("loading"),
  cartCount: state => {
    return (state.cart && state.cart.items.length) || 0;
  }
};
const actions = {
  async addToCart({ commit, dispatch }, slug) {
    commit("setLoading", 1);
    console.log("products/addToCart");
    try {
      await this.$axios.$post("/api/cart/add/", slug);
      await dispatch("fetchCart");
      this.$toast.success("cart updated");
    } catch (err) {
      console.log(err.response);
      commit("setLoading", 3);
    }
  },
  async removeFromCart({ commit, dispatch }, id) {
    commit("setLoading", 1);
    console.log("products/addToCart");
    try {
      await this.$axios.$delete(`/api/cart/${id}/delete/`);
      await dispatch("fetchCart");
      this.$toast.success("cart updated");
    } catch (err) {
      console.log(err.response);
      commit("setLoading", 3);
    }
  },
  async updateItemCart({ commit, dispatch }, slug) {
    commit("setLoading", 1);
    console.log("products/updateItemCart");
    try {
      await this.$axios.$post(`/api/cart/update/`, slug);
      await dispatch("fetchCart");
      this.$toast.success("cart updated");
    } catch (err) {
      console.log(err.response);
      // this.$toast.error(err);
      commit("setLoading", 3);
    }
  },
  async fetchCart({ commit }) {
    commit("setLoading", 1);
    try {
      const data = await this.$axios.$get("/api/cart/");
      // todo update cart state
      console.log("fetchCart", data);
      commit("setCart", data);
      commit("setLoading", 2);
    } catch (err) {
      console.log(err.response.data);
      // this.$toast.success(err);
      commit("setLoading", 3);
    }
  },
  async addCoupon({ commit, dispatch }, code) {
    commit("setLoading", 1);
    try {
      await this.$axios.$post("/api/coupon/add/", code);
      await dispatch("fetchCart");
      return true;
    } catch (err) {
      if (parseInt(err.response.status) in [400, 401]) {
        this.$toast.error(err.response.data.detail);
      }
      console.log(err.response);
      commit("setLoading", 3);
    }
  },
  async checkout({ commit, dispatch }, data) {
    commit("setLoading", 1);
    try {
      await this.$axios.$post("/api/checkout/", data);
      await dispatch("fetchCart");
      return true;
    } catch (err) {
      console.log(err.response);
      commit("setLoading", 3);
    }
  },
  clear({ commit }) {
    commit("setCart", {});
  }
};
const mutations = {
  setCart: set("cart"),
  setLoading: set("loading")
};

export default {
  state,
  getters,
  actions,
  mutations
};
