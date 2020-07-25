<router>
  {
    name: ''
  }
</router>
<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="4">
        <v-card height="auto" width="100%">
          <v-list dense nav>
            <v-list-item
              v-for="item in links"
              :key="item.title"
              link
              :to="item.link"
            >
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>

              <v-list-item-content>
                <v-list-item-title class="text-capitalize">{{
                  item.title
                }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
      <v-col cols="12" md="8">
        <v-card>
          <v-card-text>
            <nuxt-child></nuxt-child>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  middleware: ["auth"],
  head() {
    return {
      title: "My Profile",
      meta: [
        {
          hid: "description",
          name: "description",
          content: "Profile page"
        }
      ]
    };
  },
  async fetch({ store }) {
    await store.dispatch("profile/fetchAddresses");
    await store.dispatch("profile/fetchCountries");
    await store.dispatch("profile/fetchOrders");
  },

  data() {
    return {
      links: [
        {
          title: "address data",
          icon: "mdi-account-details",
          link: { name: "profile-address" }
        },
        {
          title: "order history",
          icon: "mdi-history",
          link: { name: "profile-orders" }
        },
        {
          title: "change password",
          icon: "mdi-key-change",
          link: { name: "profile-change-password" }
        }
      ]
    };
  },

  computed: {},
  methods: {}
};
</script>

<style></style>
