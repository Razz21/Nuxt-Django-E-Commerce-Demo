<template>
  <div>
    <div class="title mb-5">My addresses</div>
    <v-data-table
      :headers="headers"
      :items="addresses"
      :items-per-page="5"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-btn
            color="primary"
            dark
            class="mb-2"
            @click="dialog = true"
            :loading="loading === 1"
            >New Address</v-btn
          >
        </v-toolbar>
      </template>

      <template v-slot:no-data>
        <div class="text-center">
          <div class="title">You do not have any specified Addresses</div>
          <div class="subtitle">Add new address to complete your orders.</div>
        </div>
      </template>

      <template v-slot:item.address_type="{ item }">
        <div v-if="item.address_type === 'B'">Billing</div>
        <div v-else-if="item.address_type === 'S'">Shipping</div>
      </template>

      <template v-slot:item.default="{ item }">
        <v-icon v-if="item.default" color="green">mdi-check-circle</v-icon>
      </template>
      <template v-slot:item.action="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)">
          mdi-pencil
        </v-icon>
        <v-icon small @click="deleteItem(item)">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
    <v-dialog v-model="dialog" max-width="500px" persistent>
      <AddressForm
        :loading="loading === 1"
        :edit="edit"
        :countries="countries"
        :editData="editData"
        @submit="saveAddress"
        @close="close"
      />
    </v-dialog>
  </div>
</template>

<script>
import AddressForm from "@/components/Profile/AddressForm";
export default {
  components: { AddressForm },
  head() {
    return {
      title: "Address",
      meta: [
        {
          hid: "description",
          name: "description",
          content: "Address data"
        }
      ]
    };
  },
  data() {
    return {
      dialog: false,
      edit: false,
      headers: [
        { text: "Type", align: "left", value: "address_type" },
        { text: "St.", value: "street_address" },
        { text: "Apt.", value: "apartment_address" },
        { text: "Ctry", value: "country" },
        { text: "ZIP", value: "zip" },
        { text: "default", value: "default" },
        { text: "Actions", value: "action", sortable: false }
      ],
      defaultData: {
        address_type: "S",
        street_address: "",
        apartment_address: "",
        zip: "",
        country: "",
        default: false
      },
      editData: {
        address_type: "S",
        street_address: "",
        apartment_address: "",
        zip: "",
        country: "",
        default: false
      }
    };
  },
  computed: {
    countries() {
      return this.$store.getters["profile/getCountries"];
    },
    addresses() {
      return this.$store.getters["profile/getAddresses"];
    },
    loading() {
      return this.$store.getters["profile/getloading"];
    }
  },
  methods: {
    saveAddress(data) {
      let action = "profile/createAddress";
      if (data.edit) {
        action = "profile/updateAddress";
      }
      this.$store.dispatch(action, data.formData).then(() => {
        this.close();
      });
    },
    close() {
      this.dialog = false;
      this.edit = false;
      this.editData = Object.assign({}, this.defaultData);
    },
    editItem(item) {
      this.editData = Object.assign({}, item);
      this.edit = true;
      this.dialog = true;
    },
    deleteItem(item) {
      confirm("Are you sure you want to delete this item?") &&
        this.$store.dispatch("profile/deleteAddress", item.id);
    }
  }
};
</script>

<style scoped>
.v-dialog__content .v-dialog {
  display: unset !important;
}
</style>
