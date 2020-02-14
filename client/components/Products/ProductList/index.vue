<template>
  <v-row>
    <v-col cols="6" sm="4" md="6" lg="4" v-for="item in items" :key="item.id">
      <slot :item="item">
        <ProductCard :item="item" />
      </slot>
    </v-col>
  </v-row>
</template>

<script>
import ProductCard from "@/components/Products/ProductCard";
export default {
  components: { ProductCard },
  props: {
    items: Array
  }
};
</script>

<style></style>
