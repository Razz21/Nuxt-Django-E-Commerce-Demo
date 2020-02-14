<template>
  <span
    class="label d-inline-block accent-2 caption text--darken-4 font-weight-medium"
    :class="[color]"
    >{{ name }}</span
  >
</template>

<script>
export default {
  props: ["name"],
  computed: {
    color() {
      switch (this.name.toLowerCase()) {
        case "new":
          return "green";
        case "popular":
          return "light-blue";
        case "discount":
          return "red";
        default:
          return;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.label {
  border-radius: 10px !important;
  padding: 3px 6px;
  position: absolute;
  top: -13px;
}
</style>
