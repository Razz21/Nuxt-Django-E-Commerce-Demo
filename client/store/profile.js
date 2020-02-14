import {
  set,
  get,
  LOADING_HANDLERS,
  returnRequest,
  queryAction,
  getPaginatedResults
} from "~/utils";

const state = () => ({
  addresses: [],
  countries: [],
  loading: 0,
  orders: []
});
const getters = {
  getLoading: get("loading"),
  getAddresses: get("addresses"),
  getCountries: get("countries"),
  getOrders: get("orders")
};

const actions = {
  async fetchAddresses({ commit }) {
    const retrieveData = returnRequest(this.$axios.$get("/api/address/"));
    const action = queryAction(
      retrieveData,
      getPaginatedResults,
      "setAddresses",
      LOADING_HANDLERS
    );
    await action.run({ commit });
  },
  async createAddress({ commit, dispatch }, data) {
    commit("setLoading", 1);
    try {
      await this.$axios.$post("/api/address/", data);
      console.log("createAddress");
      await dispatch("fetchAddresses");
      return true;
    } catch (err) {
      console.log(err);
      commit("setLoading", 3);
    }
  },
  async updateAddress({ commit, dispatch }, data) {
    commit("setLoading", 1);
    console.log("updateAddress");
    try {
      await this.$axios.$put(`/api/address/${data.id}/`, data);
      await dispatch("fetchAddresses");
      return true;
    } catch (err) {
      console.log(err);
      commit("setLoading", 3);
    }
  },
  async deleteAddress({ commit, dispatch }, id) {
    commit("setLoading", 1);
    try {
      await this.$axios.$delete(`/api/address/${id}`);
      console.log("deleteAddress");
      await dispatch("fetchAddresses");
    } catch (err) {
      console.log(err);
      commit("setLoading", 3);
    }
  },
  async fetchCountries({ commit, state }) {
    // fetch only once - data do not change
    if (state.countries.length) return;
    const fn = data => {
      return Object.keys(data).map(k => {
        return { value: k, text: data[k] };
      });
    };
    const retrieveData = returnRequest(this.$axios.$get("/api/country-list/"));
    const action = queryAction(retrieveData, fn, "setCountries", {
      ...LOADING_HANDLERS
    });
    await action.run({ commit });
  },
  async fetchOrders({ commit }) {
    const retrieveData = returnRequest(this.$axios.$get("/api/orders/"));
    const action = queryAction(
      retrieveData,
      getPaginatedResults,
      "setOrders",
      LOADING_HANDLERS
    );
    await action.run({ commit });
  },
  clear({ commit }) {
    commit("setAddresses", []);
    commit("setCountries", []);
    commit("setOrders", []);
  }
};
const mutations = {
  setLoading: set("loading"),
  setAddresses: set("addresses"),
  setCountries: set("countries"),
  setOrders: set("orders")
};

export default {
  state,
  getters,
  actions,
  mutations
};
