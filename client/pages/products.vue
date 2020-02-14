<router>
  {
    name: ''
  }
</router>
<template>
  <div>
    <Flipper :flip-key="$route.fullPath" stagger="gentle">
      <div>
        <keep-alive :exclude="['products-slug']">
          <router-view :key="$route.fullPath" />
        </keep-alive>
      </div>
    </Flipper>
  </div>
</template>

<script>
// todo keep alive <products list> data when switching with <detail page>
// https://github.com/nuxt/nuxt.js/pull/5947
import { Flipper } from "vue-flip-toolkit";
export default {
  // transition: { mode: "in-out" },
  components: { Flipper }
};
</script>

<style></style>
