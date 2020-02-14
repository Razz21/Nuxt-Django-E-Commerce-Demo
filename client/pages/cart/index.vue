<template>
  <v-container>
    <v-card flat class="shadow-md">
      <v-card-title class="pl-0">
        <div class="badge primary white--text">
          <div>Your Cart</div>
        </div>
      </v-card-title>
      <v-simple-table fixed-header class="cart-table">
        <thead>
          <tr>
            <th class="primary-light" width="50"></th>
            <th class="text-center primary-light">Item</th>
            <th class="text-center primary-light">Qty</th>
            <th class="text-center primary-light">Total</th>
          </tr>
        </thead>
        <tbody align="center">
          <v-fade-transition leave-absolute>
            <template v-if="cart && cart.items.length">
              <tr v-for="ob in cart.items" :key="ob.id">
                <td>
                  <v-btn icon small @click="removeFromCart(ob.id)">
                    <v-icon>mdi-close</v-icon>
                  </v-btn>
                </td>
                <td align="left">
                  <div class="d-flex align-center flex-wrap">
                    <v-img
                      :src="ob.item.image"
                      max-width="100"
                      height="80"
                      :alt="ob.item.name"
                      contain
                    ></v-img>
                    <div class="body-2 grey--text text--darken-2">
                      <div>{{ ob.item.name }}</div>
                      <div>
                        {{ ob.item.discount_price || ob.item.price | currency }}
                      </div>
                    </div>
                  </div>
                </td>
                <td>
                  <QuantityInput
                    :value="ob.quantity"
                    @more="addQuantity(ob.item.slug)"
                    @less="removeQuantity(ob.item.slug)"
                  />
                </td>
                <td>{{ ob.final_price | currency }}</td>
              </tr>
            </template>
            <tr v-else>
              <td colspan="4" class="text-center pa-4 " style="height:200px">
                <div class="title text-no-wrap">
                  Your cart is empty now
                </div>
                <p>
                  Add products to your basket
                </p>
              </td>
            </tr>
          </v-fade-transition>
        </tbody>
        <tfoot align="right">
          <td colspan="4">
            <div class="py-3 px-2">
              <div class="title font-weight-regular">
                Total: {{ cart.subtotal | currency }}
              </div>
              <v-btn
                color="primary"
                class="mt-3"
                nuxt
                depressed
                :disabled="!cartCount"
                tile
                large
                :to="{ name: 'checkout' }"
                >Checkout</v-btn
              >
            </div>
          </td>
        </tfoot>
      </v-simple-table>
    </v-card>
  </v-container>
</template>

<script>
import QuantityInput from "@/components/Cart/QuantityInput";
export default {
  middleware: "auth",
  head() {
    return {
      title: "My Cart"
    };
  },
  components: { QuantityInput },
  computed: {
    cart() {
      return this.$store.getters["cart/getCart"];
    },
    cartCount() {
      return this.$store.getters["cart/cartCount"];
    }
  },
  methods: {
    async addQuantity(slug) {
      await this.$store.dispatch("cart/addToCart", { slug });
    },
    async removeQuantity(slug) {
      await this.$store.dispatch("cart/updateItemCart", { slug });
    },
    async removeFromCart(id) {
      await this.$store.dispatch("cart/removeFromCart", id);
    }
  }
};
</script>

<style lang="scss">
.badge {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 0.5rem;
  position: relative;
  &::before {
    background-color: inherit;
    background-repeat: repeat;
    background-position: 0 0;
    background-attachment: scroll;
    content: "";
    height: 100%;
    position: absolute;
    right: -25px;
    transform: skew(-20deg);
    width: 50px;
  }
}

.cart-table {
  table {
    border-collapse: collapse;
    td,
    th {
      padding: 0 5px;
    }
  }
  tfoot {
    td {
      padding: 0.5rem;
    }
  }
  tbody {
    border-bottom: 2px solid #eee;
    td {
      white-space: nowrap;
      &:nth-child(n + 3) {
        max-width: 20%;
        min-width: 100px;
      }
    }
  }
}
</style>
