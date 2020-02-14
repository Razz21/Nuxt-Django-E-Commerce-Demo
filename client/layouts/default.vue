<template>
  <v-app dark class="d-flex flex-column white-color">
    <client-only>
      <Navbar @toggle-drawer="$refs.drawer.drawer = !$refs.drawer.drawer" />
      <Drawer ref="drawer" v-if="isMobile" />
      <AuthDialog />
    </client-only>

    <v-content class="">
      <v-container fluid fill-height class="pa-0 ">
        <v-container fluid class="pa-0 h-full">
          <nuxt />
        </v-container>
      </v-container>
    </v-content>
    <Footer />
  </v-app>
</template>

<script>
import Navbar from "@/components/UI/Navbar/Navbar";
import Drawer from "@/components/UI/Drawer";
import Footer from "@/components/UI/Footer";
import AuthDialog from "@/components/Auth/Dialog";
export default {
  components: {
    Navbar,
    Drawer,
    Footer,
    AuthDialog
  }
};
</script>

<style lang="scss">
.v-application {
  font-family: "Prompt", sans-serif !important;
}
body {
  background-color: #fff;
}
html,
body {
  min-width: 360px;
}

.container {
  @include breakpoint(xl) {
    max-width: 1385px;
  }
}
</style>
