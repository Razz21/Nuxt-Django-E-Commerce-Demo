<template>
  <v-card>
    <v-img :src="item.image" height="200px"></v-img>
    <nuxt-link :to="{ name: 'products-slug', params: { slug: item.slug } }">
      <v-card-title>{{ item.name }}</v-card-title>
    </nuxt-link>
    <v-card-subtitle>Price {{ item.price | currency }}</v-card-subtitle>
    <v-btn @click.stop="addToCart(item.slug)">add to cart</v-btn>
  </v-card>
</template>

<script>
export default {
  props: {
    item: Object
  },
  methods: {
    async addToCart(slug) {
      await this.$store.dispatch("cart/addToCart", { slug });
    }
  }
};
</script>

<style></style>
