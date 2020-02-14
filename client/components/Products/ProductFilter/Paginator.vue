<template>
  <v-pagination
    v-model="pagination.page"
    :page="pagination.page"
    :length="pagination.total_pages"
    total-visible="5"
  ></v-pagination>
</template>

<script>
export default {
  props: {
    pagination: {
      type: Object
    }
  }
};
</script>

<style></style>
