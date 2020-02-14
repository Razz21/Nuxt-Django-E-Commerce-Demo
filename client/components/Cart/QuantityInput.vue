<template>
  <div class="wrapper text-center d-flex align-center overflow-hidden">
    <v-btn @click="$emit('less')" text>&#45;</v-btn>
    <span class="flex-grow-1">{{ value }}</span>
    <v-btn @click="$emit('more')" text>&#43;</v-btn>
  </div>
</template>

<script>
export default {
  props: {
    value: Number
  },
  methods: {}
};
</script>

<style scoped lang="scss">
.wrapper {
  max-width: 120px;

  height: 25px;
  box-sizing: content-box;
  span {
    font-size: 1rem;
    padding: 8px;
    line-height: 1rem;
  }
  .v-btn {
    font-weight: 300;
    min-width: 0;
    font-size: 30px;
    width: 25px;
  }
}
</style>
