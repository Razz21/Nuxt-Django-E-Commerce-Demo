<template>
  <v-card :loading="loading" :disabled="loading">
    <v-card-title>Address</v-card-title>
    <v-card-text>
      <v-form lazy-validation v-model="valid" ref="form">
        <v-text-field
          label="Street"
          v-model="formData.street_address"
          :rules="required"
        ></v-text-field>
        <v-text-field
          label="Apartment"
          v-model="formData.apartment_address"
          :rules="required"
        ></v-text-field>
        <v-text-field
          label="Zip"
          v-model="formData.zip"
          :rules="required"
        ></v-text-field>
        <v-select
          label="Country"
          :items="countries"
          item-text="text"
          item-value="value"
          filter
          v-model="formData.country"
          :rules="required"
        ></v-select>
        <v-select
          label="Address Type"
          :items="types"
          item-text="text"
          item-value="value"
          v-model="formData.address_type"
          :rules="required"
        >
        </v-select>
        <v-checkbox
          v-model="formData.default"
          :label="`Make default`"
        ></v-checkbox>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary darken-1" text @click="close">Cancel</v-btn>
      <v-btn color="primary darken-1" text @click="submit">Save</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    countries: Array,
    edit: {
      type: Boolean,
      default: false
    },
    editData: Object,
    loading: Boolean
  },
  data() {
    return {
      required: [v => !!v || "This field is required"],
      types: [
        { text: "Shipping", value: "S" },
        { text: "Billing", value: "B" }
      ],
      valid: false,
      formData: Object.assign({}, this.editData)
    };
  },
  methods: {
    submit() {
      if (this.$refs.form.validate()) {
        const { formData, edit } = this;
        this.$emit("submit", { formData, edit });
      }
    },
    close() {
      this.$refs.form.resetValidation();
      this.$emit("close");
    }
  },
  watch: {
    editData: {
      handler() {
        this.formData = Object.assign({}, this.editData);
      },
      deep: true
    }
  }
};
</script>

<style></style>
