<template>
  <auth-form title="Password Reset" :alert="alert">
    <v-fade-transition leave-absolute>
      <div v-if="message" class="subtitle-1 text-center" v-html="message"></div>
      <v-form
        v-else
        lazy-validation
        ref="form"
        v-model="valid"
        @submit.prevent="validate"
      >
        <v-text-field
          filled=""
          v-model="email"
          :rules="emailRules"
          label="E-mail"
          required
          validate-on-blur
        ></v-text-field>

        <v-btn dark block depressed large color="primary" type="submit"
          >Send</v-btn
        >
      </v-form>
    </v-fade-transition>

    <template #actions>
      Have an account?{{ "&nbsp;" }}
      <span
        @click="$store.commit('user/setDialog', 'login')"
        class="auth-link font-weight-medium"
        >Log In</span
      >
    </template>
  </auth-form>
</template>

<script>
const required = v => !!v || "This field is required";
import AuthForm from "./Form";
export default {
  components: { AuthForm },
  data: () => ({
    valid: false,
    message: "",
    email: "",
    alert: null,
    emailRules: [required, v => /.+@.+\..+/.test(v) || "Invalid E-mail"]
  }),

  methods: {
    validate() {
      if (this.$refs.form.validate()) {
        this.$store
          .dispatch("user/resetPassword", {
            email: this.email
          })
          .then(data => {
            this.alert = {
              type: "info",
              detail:
                "This is just a demo application and no real email has been sent."
            };
            this.message = data.detail;
          });
      }
    }
  }
};
</script>
