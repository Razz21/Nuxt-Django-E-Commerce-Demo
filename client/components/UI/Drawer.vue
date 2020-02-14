<template>
  <v-navigation-drawer v-model="drawer" clipped app style="z-index:20">
    <v-list>
      <template v-for="(item, index) in items">
        <v-subheader
          class="text-capitalize py-1"
          style="height:auto"
          v-if="item.header"
          :key="item.header"
          v-text="item.header"
        ></v-subheader>
        <v-divider
          class="my-3"
          v-else-if="item.divider"
          :key="index"
          :inset="item.inset"
        ></v-divider>
        <v-list-item
          v-else
          :key="index"
          nuxt
          :to="item.link"
          exact
          :class="
            $route.name === item.link.name &&
              JSON.stringify($route.params) ===
                JSON.stringify(item.link.params) &&
              'v-list-item--active'
          "
        >
          <v-list-item-content>
            <v-list-item-title class="text-capitalize">{{
              item.title
            }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </template>
    </v-list>
    <template v-slot:append>
      <div class="pa-2" v-if="$auth.loggedIn">
        <v-btn block color="primary" @click="logout">Logout</v-btn>
      </div>
      <div class="pa-2" v-else>
        <v-btn
          block
          outlined
          color="secondary"
          @click="$store.commit('user/setDialog', 'register')"
          >Sign Up</v-btn
        >
        <v-btn
          block
          color="primary"
          class="mt-2"
          @click="$store.commit('user/setDialog', 'login')"
          >Login</v-btn
        >
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
export default {
  data() {
    return {
      drawer: null,
      items: [
        { title: "Home", link: { name: "index" } },
        { divider: true },
        { header: "Products" },
        { title: "All", link: { name: "products" } },
        {
          title: "Chair",
          link: { name: "products-category", params: { slug: "chair" } }
        },
        {
          title: "Table",
          link: { name: "products-category", params: { slug: "table" } }
        },
        {
          title: "Shelf",
          link: { name: "products-category", params: { slug: "shelf" } }
        },
        { divider: true },
        { header: "Profile" },
        { title: "My Account", link: { name: "profile" } }
      ]
    };
  },
  methods: {
    logout() {
      this.$store.dispatch("user/logout");
    }
  }
};
</script>

<style></style>
