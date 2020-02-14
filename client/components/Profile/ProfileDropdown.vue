<template>
  <v-card
    min-height="150"
    min-width="150"
    flat
    color="transparent"
    class="relative d-flex"
  >
    <div v-if="!$auth.loggedIn" class="d-flex flex-column text-center ">
      <v-card-text class="d-flex justify-center align-center flex-grow-1">
        Please Log in to continue
      </v-card-text>

      <v-btn
        class="flex-grow-0"
        @click="$router.push({ name: 'login' })"
        block
        tile
        depressed
        color="primary"
        >Login</v-btn
      >
    </div>
    <v-list v-else dense>
      <v-list-item v-for="item in items" :key="item.title" :to="item.link">
        <v-list-item-icon>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title v-text="item.title"></v-list-item-title>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item @click="$store.dispatch('user/logout')">
        <v-list-item-icon>
          <v-icon>mdi-logout-variant</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      items: [
        {
          title: "My Address",
          link: { name: "profile-address" },
          icon: "mdi-home-plus"
        },
        {
          title: "My Orders",
          link: { name: "profile-orders" },
          icon: "mdi-history"
        },
        {
          title: "Change Password",
          link: { name: "profile-change-password" },
          icon: "mdi-lock-reset"
        }
      ]
    };
  }
};
</script>

<style></style>
