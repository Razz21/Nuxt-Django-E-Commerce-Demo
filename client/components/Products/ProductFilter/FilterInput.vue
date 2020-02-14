<template>
  <div>
    <div class="d-flex justify-space-between grey--text text--darken-1">
      <div class="text-capitalize title">{{ title }}</div>
      <div>
        <v-btn @click="open = !open" icon>
          <v-icon v-if="open">mdi-minus</v-icon>
          <v-icon v-else>mdi-plus</v-icon>
        </v-btn>
      </div>
    </div>

    <v-divider class="mt-2 mb-4"></v-divider>
    <div v-expand="open">
      <div class="pa-2">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: String
  },
  data() {
    return {
      open: true
    };
  }
};
</script>

<style lang="scss"></style>
