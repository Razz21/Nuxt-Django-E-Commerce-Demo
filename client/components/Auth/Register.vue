<template>
  <auth-form title="Sign Up">
    <v-form
      lazy-validation
      ref="form"
      v-model="valid"
      @submit.prevent="validate"
    >
      <v-text-field
        filled=""
        v-model="username"
        label="Username"
        :rules="requiredRule"
        required
        validate-on-blur
      ></v-text-field>

      <v-text-field
        filled=""
        v-model="email"
        :rules="emailRules"
        label="E-mail"
        required
        validate-on-blur
      ></v-text-field>

      <v-text-field
        filled
        validate-on-blur
        v-model="password1"
        :rules="passwordRules"
        label="Password"
        required
        :type="show1 ? 'text' : 'password'"
        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append="show1 = !show1"
      ></v-text-field>

      <v-text-field
        filled
        validate-on-blur
        v-model="password2"
        :rules="password2Rules"
        label="Type password again"
        required
        :type="show2 ? 'text' : 'password'"
        :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append="show2 = !show2"
      ></v-text-field>
      <v-btn dark block depressed large color="primary" type="submit"
        >Sign Up</v-btn
      >
    </v-form>

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
    show1: false,
    show2: false,
    username: "",
    password1: "",
    password2: "",
    requiredRule: [required],
    passwordRules: [
      required,
      //   todo password validation
      v =>
        (v && v.length >= 6) || "Password length must be more than 6 characters"
    ],

    email: "",
    emailRules: [required, v => /.+@.+\..+/.test(v) || "Invalid E-mail"]
  }),
  computed: {
    password2Rules() {
      return [
        ...this.passwordRules,
        () => this.password2 === this.password1 || "Passwords do not match"
      ];
    }
  },

  methods: {
    async validate() {
      if (this.$refs.form.validate()) {
        const { email, password1, password2, username } = this;
        this.$store.dispatch("user/register", {
          email,
          password1,
          password2,
          username
        });
      }
    }
  }
};
</script>
