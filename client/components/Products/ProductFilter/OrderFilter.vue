<template>
  <v-select
    class="select"
    filled
    dense
    :value="ordering"
    @change="$emit('update:ordering', $event)"
    :items="order_types"
    hide-details
    single-line
    item-value="value"
    hide-selected
    label="Ordering"
  >
    <template v-slot:selection="{ item }">
      <div v-html="item.text" />
    </template>
    <template v-slot:item="{ item }"> <div v-html="item.text" /> </template>
  </v-select>
</template>

<script>
export default {
  props: {
    ordering: String,
    order_types: Array
  },
  data() {
    return {};
  }
};
</script>

<style scoped>
.v-select__selections input {
  display: none;
}
.select {
  max-width: 180px;
}
</style>
