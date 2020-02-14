<template>
  <auth-form title="Login">
    <v-form
      lazy-validation
      ref="form"
      v-model="valid"
      @submit.prevent="validate"
    >
      <v-text-field
        filled
        v-model="username"
        :rules="required"
        validate-on-blur
        label="username"
        required
      ></v-text-field>

      <v-text-field
        filled
        validate-on-blur
        type="password"
        v-model="password"
        :rules="passwordRules"
        label="Password"
        required
      ></v-text-field>
      <div
        class="caption auth-link font-weight-medium"
        @click="$store.commit('user/setDialog', 'reset')"
      >
        Forgot password?
      </div>
      <input type="submit" hidden />
      <v-btn dark block depressed large color="primary" type="submit"
        >Log in</v-btn
      >
    </v-form>

    <template #actions>
      Don’t have an account yet?{{ "&nbsp;" }}
      <span
        @click="$store.commit('user/setDialog', 'register')"
        class="auth-link font-weight-medium"
        >Sign Up</span
      >
    </template>
  </auth-form>
</template>

<script>
import AuthForm from "./Form";
export default {
  components: { AuthForm },
  data() {
    return {
      valid: false,
      password: "",
      passwordRules: [v => !!v || "Password is required"],
      username: "",
      required: [v => !!v || "This field is required"],
      emailRules: [
        v => !!v || "E-mail is required",
        v => /.+@.+\..+/.test(v) || "Invalid E-mail"
      ]
    };
  },
  mounted() {
    this.$refs.form.reset();
  },

  methods: {
    async validate() {
      if (this.$refs.form.validate()) {
        const { username, password } = this;
        await this.$store.dispatch("user/login", { username, password });
      }
    }
  }
};
</script>
