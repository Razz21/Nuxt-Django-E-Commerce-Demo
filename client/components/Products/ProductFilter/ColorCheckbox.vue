<template>
  <label>
    <input type="checkbox" :checked="checked" :value="color.id" />
    <span :style="{ color: color.hex }"></span>
  </label>
</template>

<script>
export default {
  props: { color: Object, checked: Boolean },
  data() {
    return {};
  }
};
</script>

<style lang="scss" scoped>
label {
  display: inline-flex;
  align-items: baseline;
  justify-content: center;
  cursor: pointer;
  position: relative;
}
input {
  -moz-appearance: none;
  appearance: none;
  font-size: inherit;
  width: 20px;
  margin: 0;
  color: inherit;
  outline: none;

  &:checked + span {
    &::before {
      transform: scale(1.3);
      opacity: 1;
    }
    &::after {
      transform: scale(0.5);
    }
  }
  & + span {
    display: inline-flex;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    position: relative;
    top: 0;
    left: 0;
    transition-property: opacity, transform;
    transition-duration: 0.4s;
    transition-timing-function: ease;
    color: #80aadb;

    &::after,
    &::before {
      content: "";
      box-sizing: border-box;
      transition: inherit;
      border-radius: 100%;
      width: 100%;
      height: 100%;
      position: absolute;
      top: 0px;
      left: 0px;
    }
    &::after {
      background-color: currentcolor;
    }
    &::before {
      border: 1px solid;
      opacity: 0;
    }
  }
}
</style>
