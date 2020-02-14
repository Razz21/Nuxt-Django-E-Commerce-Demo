const state = () => ({});
const getters = {};
const actions = {
  async nuxtServerInit({ dispatch }, { $auth }) {
    if ($auth.user) {
      await dispatch("cart/fetchCart");
    }
    await dispatch("products/fetchCategories");
    await dispatch("products/fetchLatest");
    await dispatch("products/fetchFilters");
  }
};
const mutations = {};

export default {
  state,
  getters,
  actions,
  mutations
};
