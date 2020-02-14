<template>
  <div>
    <div class="pa-2 pt-0">
      <h1 class="headline">Product categories</h1>
    </div>
    <v-list dense class="shadow-lg">
      <v-list-item
        v-for="c in categories"
        :key="c.id"
        link
        :to="{ name: 'products-category', params: { slug: c.slug } }"
      >
        <v-list-item-content>{{ c.name }}</v-list-item-content>
        <v-list-item-action>
          <v-list-item-action-text
            >({{ c.items_count }})</v-list-item-action-text
          >
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </div>
</template>

<script>
export default {
  computed: {
    categories() {
      return this.$store.getters["products/getCategories"];
    }
  }
};
</script>

<style></style>
