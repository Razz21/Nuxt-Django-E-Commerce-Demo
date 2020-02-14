import { set, get } from "~/utils";
const state = () => ({
  loading: 0,
  dialog: false
});

const getters = {
  getLoading: get("loading"),
  getDialog: get("dialog")
};

const actions = {
  logout({ commit, dispatch }) {
    commit("setLoading", 1);
    this.$auth
      .logout()
      .then(() => {
        commit("setLoading", 2);
      })
      .catch(err => {
        console.log(err.response.data);
        commit("setLoading", 3);
      })
      .finally(() => {
        dispatch("cart/clear", null, { root: true });
        dispatch("profile/clear", null, { root: true });
      });
  },
  async login({ commit, dispatch }, data) {
    commit("setLoading", 1);
    try {
      await this.$auth.loginWith("local", { data });
      await dispatch("cart/fetchCart", null, { root: true });
      commit("setLoading", 2);
      commit("setDialog", null);
    } catch (error) {
      console.log(error);
      dispatch("errorHandler", { error });

      commit("setLoading", 3);
    }
  },
  async register({ commit, dispatch }, data) {
    commit("setLoading", 1);
    try {
      await this.$axios.$post("/auth/register/", data);
      await dispatch("login", { data });
    } catch (error) {
      console.log(error.response);
      dispatch("errorHandler", { error });
      commit("setLoading", 3);
    }
  },
  resetPassword({ commit }, email) {
    commit("setLoading", 1);
    return new Promise(resolve => {
      setTimeout(() => {
        commit("setLoading", 2);
        resolve({
          detail: `Reset message has been sent to ${email.email}.<br /> Please check your email account for details.`
        });
      }, 1000);
    });
    // return this.$axios
    //   .$post("/api/auth/password/reset/", email)
    //   .then(data => {
    //     commit("setLoading", 2);
    //     return data;
    //   })
    //   .catch(error => {
    //     console.log(error);
    //     dispatch("errorHandler", { error });
    //     commit("setLoading", 3);
    //   });
  },
  confirmPassword({ commit, dispatch }, data) {
    commit("setLoading", 1);
    this.$axios
      .$post("/auth/password/reset/confirm/", data)
      .then(() => {
        commit("setLoading", 2);
        this.$toast.success("You can now login with your new password.");
        this.$router.push("/");
      })
      .catch(error => {
        console.log(error.response);
        dispatch("errorHandler", { error });
        commit("setLoading", 3);
      });
  },
  changePassword({ commit }, data) {
    commit("setLoading", 1);
    return this.$axios
      .$post("/auth/password/change/", data)
      .then(() => {
        commit("setLoading", 2);
        this.$toast.success("Password changed successfully.");
        return true;
      })
      .catch(error => {
        console.log(error.response);
        dispatch("errorHandler", { error });
        commit("setLoading", 3);
      });
  },
  errorHandler(ctx, { error, message }) {
    let msg;
    // custom message
    if (message && typeof message === "string") {
      msg = message;
      // message from server
    } else if (error.data.detail) {
      msg = error.data.detail;
    } else {
      // do not return to client unformatted errors
      msg = "An error occured. Please try again later.";
    }
    this.$toast.error(msg);
  }
};

const mutations = {
  setLoading: set("loading"),
  setDialog: set("dialog")
};

export default {
  state,
  getters,
  actions,
  mutations
};
