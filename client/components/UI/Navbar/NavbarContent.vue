<template>
  <Flipper :flip-key="currentIndex" class="h-full w-full">
    <v-container
      class="d-flex flex-nowrap align-center h-full py-0"
      @mouseleave="onMouseLeave"
      :class="{ 'px-0': isMobile }"
    >
      <v-app-bar-nav-icon
        v-if="isMobile"
        @click.stop="$emit('toggle-drawer')"
      ></v-app-bar-nav-icon>
      <nuxt-link to="/" style="text-decoration:none; color:black" class="mr-5">
        <v-toolbar-title class="font-weight-black">
          TAKT
        </v-toolbar-title>
      </nuxt-link>
      <v-spacer></v-spacer>

      <template v-if="!isMobile">
        <SearchDesktop />
        <v-spacer></v-spacer>

        <div class="center-items d-flex">
          <v-btn
            v-for="item in productLinks"
            :key="item.text"
            :to="item.path"
            nuxt
            class="btn-nav ml-auto"
            tile
            text
            exact
            :class="
              $route.name === item.path.name &&
                JSON.stringify($route.params) ===
                  JSON.stringify(item.path.params) &&
                'v-btn--active'
            "
          >
            {{ item.text }}
          </v-btn>
        </div>
        <v-spacer></v-spacer>
      </template>

      <v-btn icon v-if="isMobile" @click="$emit('toggle-search')">
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

      <div class="d-flex">
        <nav-item @itemEnter="onMouseEnter" :index="0">
          <template #activator>
            <v-btn icon :to="{ name: 'profile' }">
              <v-icon>mdi-account</v-icon>
            </v-btn>
          </template>
          <DropdownContainer v-if="currentIndex === 0">
            <ProfileDropdown />
          </DropdownContainer>
        </nav-item>

        <nav-item @itemEnter="onMouseEnter" :index="1">
          <template #activator>
            <v-badge overlap bottom :content="cartCount" :value="cartCount">
              <v-btn icon :to="{ name: 'cart' }">
                <v-icon>mdi-shopping</v-icon>
              </v-btn>
            </v-badge>
          </template>
          <DropdownContainer v-if="currentIndex === 1">
            <CartDropdown />
          </DropdownContainer>
        </nav-item>
      </div>
    </v-container>
  </Flipper>
</template>

<script>
import CartDropdown from "@/components/Cart/CartDropdown";
import ProfileDropdown from "@/components/Profile/ProfileDropdown";
import NavItem from "./NavItem";
import DropdownContainer from "./DropdownContainer";
import NavbarContent from "./NavbarContent";
import SearchDesktop from "./SearchDesktop";
import { Flipper, Flipped } from "vue-flip-toolkit";

export default {
  components: {
    NavItem,
    DropdownContainer,
    Flipper,
    CartDropdown,
    ProfileDropdown,
    Flipped,
    SearchDesktop,
    NavbarContent
  },
  data() {
    return {
      productLinks: [
        { text: "All", path: { name: "products", params: {} } },
        {
          text: "Chair",
          path: { name: "products-category", params: { slug: "chair" } }
        },
        {
          text: "Table",
          path: { name: "products-category", params: { slug: "table" } }
        },
        {
          text: "shelf",
          path: { name: "products-category", params: { slug: "shelf" } }
        }
      ],
      activeIndices: []
    };
  },
  computed: {
    cartCount() {
      return this.$store.getters["cart/cartCount"];
    },
    currentIndex() {
      return this.activeIndices[this.activeIndices.length - 1];
    }
  },
  methods: {
    logout() {
      this.$store.dispatch("user/logout");
    },
    openDialog(val) {
      this.$store.commit("user/setDialog", val);
    },
    onMouseLeave() {
      this.activeIndices = [];
    },
    onMouseEnter(i) {
      if (this.activeIndices[this.activeIndices.length - 1] === i) return;
      this.activeIndices = this.activeIndices.concat(i);
    }
  }
};
</script>

<style lang="scss">
.btn-nav {
  font-size: 0.7rem !important;
  font-weight: 500;
  color: #666 !important;
}

.center-items {
  // position: absolute;
  // left: 50%;
  // transform: translateX(-50%);
  height: 100%;
  > button,
  > a {
    flex: 1 0 0 !important;
    height: 100% !important;
  }
}

.v-toolbar__title {
  @extend .page-title;
}
.v-btn--active {
  // background-color: $primary-light;
  color: $primary !important;
}
</style>
