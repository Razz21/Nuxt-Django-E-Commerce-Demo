<template>
  <v-app-bar
    tile
    clipped-left
    app
    fixed
    flat
    elevation="1"
    :height="$vuetify.breakpoint.mdAndUp ? 80 : undefined"
    class="my-nav"
    style="z-index:10"
  >
    <transition :name="transitionName" mode="out-in">
      <SearchMobile v-if="search && isMobile" @toggle-search="search = false" />

      <NavbarContent @toggle-search="search = true" v-on="$listeners" v-else />
    </transition>
  </v-app-bar>
</template>

<script>
import NavbarContent from "./NavbarContent";
import SearchMobile from "./SearchMobile";
import { Flipper, Flipped } from "vue-flip-toolkit";

export default {
  components: {
    NavbarContent,
    SearchMobile
  },
  data() {
    return {
      search: false
    };
  },
  computed: {
    transitionName() {
      if (this.isMobile) {
        return "nav-fade";
      }
    }
  },
  watch: {
    isMobile() {
      this.search = false;
    }
  },
  methods: {
    toggleTheme() {
      this.$vuetify.theme.isDark = !this.$vuetify.theme.isDark;
    },
    toggleSearch() {}
  }
};
</script>

<style lang="scss">
.my-nav {
  max-width: 100vw;
  > div {
    padding: 0 1rem !important;
    > a,
    > button:not(.secondary) {
      &:hover {
        background-color: #11111110 !important;
      }
    }
    button.secondary {
      &:hover {
        filter: brightness(1.1);
      }
    }
  }
}
.nav-fade {
  &-enter-active,
  &-leave-active {
    transition-duration: 0.1s;
    transition-timing-function: ease;
    transition-property: opacity, transform;
  }

  &-enter,
  &-leave-to {
    transform: translateX(-10px);
    opacity: 0;
  }
}
</style>
