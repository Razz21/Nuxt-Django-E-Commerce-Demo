<template>
  <div class="dropdown-slot">
    <Flipped flip-id="dropdown-caret">
      <div class="caret" />
    </Flipped>
    <Flipped flipId="dropdown">
      <div class="dropdown-bg" ref="bg" :style="{ '--diff': diff }">
        <Flipped inverseFlipId="dropdown" scale>
          <transition appear name="flip-fade">
            <div>
              <slot />
            </div>
          </transition>
        </Flipped>
      </div>
    </Flipped>
  </div>
</template>

<script>
import { Flipped } from "vue-flip-toolkit";
export default {
  components: { Flipped },
  data() {
    return {
      diff: 0
    };
  },

  mounted() {
    /*
    avoid viewport overflow using calculated css variable 
    to transform droprown content dynamically
     */
    // get position of dropdown's container egde
    const right = this.$refs.bg.getBoundingClientRect().right;
    const appWidth = window.app.clientWidth;
    // compare with viewport width
    // add 10px margin to right
    if (right + 10 > appWidth) {
      this.diff = right + 10 - appWidth + "px";
    }
  }
};
</script>

<style lang="scss">
.dropdown-slot {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  perspective: 1000px;
  padding-top: 10px;
}

.caret {
  position: absolute;
  display: block;
  width: 0;
  height: 0;
  border-width: 10px;
  border-style: solid;
  border-color: transparent transparent #fff;
  top: -18px;
  left: calc(50% - 10px);
  z-index: 1;
}
.dropdown-bg {
  top: -10px;
  transform: translateX(calc(var(--diff) * -1));
  transform-origin: 0 0;
  background-color: #fff;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 50px 100px rgba(50, 50, 93, 0.1),
    0 15px 35px rgba(50, 50, 93, 0.15), 0 5px 15px rgba(0, 0, 0, 0.1);
}
.flip-fade {
  &-enter-active,
  &-leave-active {
    transition: opacity 0.2s ease 0.2s;
  }

  &-enter,
  &-leave-to {
    opacity: 0;
  }
}
</style>
