<template>
  <v-dialog
    style="position:fixed"
    persistent
    :value="active"
    max-width="400px"
    :fullscreen="$vuetify.breakpoint.xs"
  >
    <v-btn icon class="closeIcon" @click="close">
      <v-icon>mdi-close</v-icon>
    </v-btn>
    <v-card flat :loading="loading" :disabled="loading" height="100%">
      <Register v-if="active === 'register'" />
      <PasswordReset v-else-if="active === 'reset'" />
      <Login v-else />
    </v-card>
  </v-dialog>
</template>

<script>
import Login from "./Login";
import Register from "./Register";
import PasswordReset from "./PasswordReset";
export default {
  components: { Login, Register, PasswordReset },
  computed: {
    active: {
      set(val) {
        this.$store.commit("user/setDialog", val);
      },
      get() {
        return this.$store.getters["user/getDialog"];
      }
    },
    loading() {
      return this.$store.getters["user/getLoading"] === 1;
    }
  },
  methods: {
    close() {
      this.active = null;
    }
  }
};
</script>

<style lang="scss" scoped>
.auth-card {
  overflow: hidden;
  & .v-card__text {
    padding: 10px 7%;
    justify-content: space-evenly;
  }
}
.v-dialog__content {
  position: fixed !important;
}
.closeIcon {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 3;
}
</style>
