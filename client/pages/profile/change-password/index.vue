<template>
  <div class="">
    <div class="title mb-5">Change Password</div>

    <v-form
      lazy-validation
      ref="form"
      v-model="valid"
      @submit.prevent="validate"
    >
      <v-text-field
        filled
        v-model="old_password"
        :rules="passwordRules"
        label="Old Password"
        required
        :type="show ? 'text' : 'password'"
        :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append="show = !show"
      ></v-text-field>

      <v-text-field
        filled
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
        v-model="new_password2"
        :rules="new_password2Rules"
        label="Type password again"
        required
        :type="show2 ? 'text' : 'password'"
        :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
        @click:append="show2 = !show2"
      ></v-text-field>
      <v-btn dark block depressed large color="secondary" type="submit"
        >Confirm</v-btn
      >
    </v-form>
  </div>
</template>

<script>
const required = v => !!v || "This field is required";

export default {
  head() {
    return {
      title: "Change Password",
      meta: [
        {
          hid: "description",
          name: "description",
          content: "Change Password data"
        }
      ]
    };
  },
  components: {},
  data: () => ({
    valid: false,
    show: false,
    show1: false,
    show2: false,
    old_password: "",
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
    new_password2Rules() {
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
        const { old_password, new_password1, new_password2 } = this;
        this.$store
          .dispatch("user/changePassword", {
            old_password,
            new_password1,
            new_password2
          })
          .then(() => this.$refs.form.reset());
      }
    }
  }
};
</script>
