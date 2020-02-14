<router>
  {
    name:'password-reset-confirm',
    path: '/password/reset/confirm/:uid/:token/',
  }
</router>
<template>
  <v-container class="d-flex align-center justify-center h-full">
    <div style="max-width:500px;min-width:350px" class="ma-auto">
      <div class="title mb-5">Set new Password</div>

      <v-form
        lazy-validation
        ref="form"
        v-model="valid"
        @submit.prevent="validate"
      >
        <v-text-field
          filled
          validate-on-blur
          v-model="new_password1"
          :rules="passwordRules"
          label="New Password"
          required
          :type="show1 ? 'text' : 'password'"
          :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="show1 = !show1"
        ></v-text-field>

        <v-text-field
          filled
          validate-on-blur
          v-model="new_password2"
          :rules="password2Rules"
          label="Type password again"
          required
          :type="show2 ? 'text' : 'password'"
          :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="show2 = !show2"
        ></v-text-field>
        <v-btn dark block depressed large color="#0da89b" type="submit"
          >Save</v-btn
        >
      </v-form>
    </div>
  </v-container>
</template>

<script>
const required = v => !!v || "This field is required";

export default {
  auth: "guest",
  components: {},
  data: () => ({
    valid: false,
    show1: false,
    show2: false,
    new_password1: "",
    new_password2: "",
    requiredRule: [required],
    passwordRules: [
      required,
      //   todo password validation
      v =>
        (v && v.length >= 6) || "Password length must be more than 6 characters"
    ]
  }),
  computed: {
    password2Rules() {
      return [
        ...this.passwordRules,
        () =>
          this.new_password1 === this.new_password2 || "Passwords do not match"
      ];
    }
  },

  methods: {
    validate() {
      if (this.$refs.form.validate()) {
        const { uid, token } = this.$route.params;
        const { new_password1, new_password2 } = this;
        this.$store.dispatch("user/confirmPassword", {
          uid,
          token,
          new_password1,
          new_password2
        });
      }
    }
  }
};
</script>
