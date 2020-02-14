<template>
  <v-card class="my-3">
    <v-card-text>
      <p>{{ address.street_address }}</p>
      <p>{{ address.apartment_address }}</p>
      <p>{{ address.zip }}, {{ address.country }}</p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: ["address"]
};
</script>

<style></style>
