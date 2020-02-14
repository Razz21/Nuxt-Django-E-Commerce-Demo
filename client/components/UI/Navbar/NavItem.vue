<template>
  <div @mouseenter="onMouseEnter" @focus="onMouseEnter">
    <div class="activator">
      <slot name="activator" />
    </div>
    <div>
      <slot />
    </div>
  </div>
</template>

<script>
export default {
  props: ["index"],
  components: {},
  methods: {
    onMouseEnter() {
      this.$emit("itemEnter", this.index);
    }
  }
};
</script>

<style lang="scss"></style>
