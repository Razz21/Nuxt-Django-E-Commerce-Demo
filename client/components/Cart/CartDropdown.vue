<template>
  <v-card min-width="200" flat color="transparent" class="">
    <v-card-title class="py-2 subtitle-1">
      Your Cart
    </v-card-title>
    <v-divider></v-divider>
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
    <v-card-text v-else-if="cartCount" style="min-width:300px">
      <v-list three-line>
        <template v-for="cartItem in cart.items">
          <v-list-item :key="cartItem.id" class="px-0">
            <v-list-item-avatar tile size="70">
              <v-img :src="cartItem.item.image" contain></v-img>
            </v-list-item-avatar>

            <v-list-item-content>
              <v-list-item-title>{{ cartItem.item.name }}</v-list-item-title>
              <v-list-item-subtitle
                >Price:
                {{ orderPrice(cartItem.item) | currency }}</v-list-item-subtitle
              >
              <v-list-item-subtitle
                >Quantity: {{ cartItem.quantity }}</v-list-item-subtitle
              >
            </v-list-item-content>

            <v-list-item-action>
              <v-btn small icon @click="removeFromCart(cartItem.id)">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>
          <v-divider :key="cartItem.id + 'd'"></v-divider>
        </template>
      </v-list>

      <div class="subtitle-1 text-right">
        Total: {{ cart.total | currency }}
      </div>
      <v-btn
        block
        class="mt-3"
        color="primary"
        depressed
        nuxt
        :to="{ name: 'checkout' }"
        >Checkout</v-btn
      >
    </v-card-text>
    <v-card-text
      v-else
      class="h-full d-flex flex-column justify-center align-center pa-4"
    >
      <div class="title text-no-wrap">
        Your cart is empty now
      </div>
      <p>
        Add products to your basket
      </p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      menu: false
    };
  },
  computed: {
    cart() {
      return this.$store.getters["cart/getCart"];
    },
    cartCount() {
      const cart = this.cart;
      return cart && cart.items ? cart.items.length : 0;
    }
  },
  methods: {
    removeFromCart(id) {
      this.$store.dispatch("cart/removeFromCart", id);
    },
    orderPrice(item) {
      return item.discount_price || item.price;
    }
  }
};
</script>

<style></style>
