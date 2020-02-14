<template>
  <div>
    <!-- <v-form ref="form" :value="valid" @change="$emit('update:valid', $event)"> -->
    <v-select
      :rules="[v => !!v || 'Please select address']"
      v-bind="$attrs"
      :label="label"
      class="mt-3"
      dense
      :items="addresses"
      :value="address"
      @change="$emit('update:address', $event)"
      item-value="id"
      return-object
      hide-details
    >
      <template v-slot:item="{ item }">
        {{ item.street_address }}, {{ item.apartment_address }},
        {{ item.country }}
      </template>
      <template v-slot:selection="{ item }">
        {{ item.street_address }}, {{ item.apartment_address }},
        {{ item.country }}
      </template>
    </v-select>
    <!-- </v-form> -->
    <div class="caption mt-2">
      Not your address?
      <nuxt-link :to="{ name: 'profile-address' }"
        >Click here to add new</nuxt-link
      >
    </div>
  </div>
</template>

<script>
export default {
  props: {
    valid: Boolean,
    address: Object,
    label: { type: String, default: "Select address" }
  },
  data() {
    return {};
  },
  computed: {
    addresses() {
      return this.$store.getters["profile/getAddresses"];
    }
  }
};
</script>

<style></style>
