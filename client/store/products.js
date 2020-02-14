import {
  set,
  get,
  LOADING_HANDLERS,
  returnRequest,
  queryAction,
  getPaginatedResults
} from "~/utils";

const state = () => ({
  loading: 0,
  categories: [],
  latest: [],
  ordering: ["name", "-name", "order_price", "-order_price"],
  filters: null
});
const getters = {
  getLoading: get("loading"),
  getCategories: get("categories"),
  getLatest: get("latest"),
  getOrdering: get("ordering"),
  getFilters: get("filters")
};
const actions = {
  async fetchProducts({ commit }, query = "") {
    const retrieveData = returnRequest(this.$axios.$get("/api" + query));
    const action = queryAction(retrieveData, null, null, LOADING_HANDLERS);
    const data = await action.run({ commit });
    return data;
  },
  async fetchDetail({ commit }, slug) {
    const retrieveData = returnRequest(
      this.$axios.$get(`/api/products/${slug}/`)
    );
    const action = queryAction(retrieveData, null, null, LOADING_HANDLERS);
    const data = await action.run({ commit });
    return data;
  },
  async fetchCategories({ commit, dispatch }) {
    const retrieveData = returnRequest(this.$axios.$get(`/api/category/`));
    const action = queryAction(
      retrieveData,
      null,
      "setCategories",
      LOADING_HANDLERS
    );
    await action.run({ commit });
  },
  async fetchLatest({ commit }) {
    const retrieveData = returnRequest(
      this.$axios.$get(`/api/products/latest/`)
    );
    const action = queryAction(
      retrieveData,
      getPaginatedResults,
      "setLatest",
      LOADING_HANDLERS
    );
    await action.run({ commit });
  },
  async fetchFilters({ commit }) {
    const retrieveData = returnRequest(this.$axios.$get(`/api/filters/`));
    const action = queryAction(
      retrieveData,
      null,
      "setFilters",
      LOADING_HANDLERS
    );
    await action.run({ commit });
  },
  async quickSearch({ commit, dispatch }, query) {
    if (!query || typeof query !== "string") return;

    const retrieveData = returnRequest(
      this.$axios.$get(`/api/products/search/?search=${query}`)
    );
    const action = queryAction(
      retrieveData,
      null,
      "setFilters",
      LOADING_HANDLERS
    );
    const data = await action.run({ commit });
    return data;
  }
};
const mutations = {
  setLoading: set("loading"),
  setCategories: set("categories"),
  setLatest: set("latest"),
  setFilters: set("filters")
};

export default {
  state,
  getters,
  actions,
  mutations
};
