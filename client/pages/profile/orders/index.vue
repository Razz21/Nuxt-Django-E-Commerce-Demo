<template>
  <div>
    <div class="title mb-5">My orders</div>
    <v-data-table
      :headers="headers"
      :items="orders"
      :expanded.sync="expanded"
      item-key="name"
      show-expand
    >
      <template v-slot:no-data>
        <div class="text-center">
          <div class="title">You do not have any completed orders</div>
        </div>
      </template>
      <template v-slot:item.payment.timestamp="{ item }">
        {{ item.payment.timestamp | locale }}
      </template>
      <template v-slot:item.subtotal="{ item }">
        {{ item.subtotal | currency }}
      </template>
      <template v-slot:item.total="{ item }">
        {{ item.total | currency }}
      </template>
      <template v-slot:item.coupon="{ item }">
        <div v-if="item.coupon">
          {{ item.coupon.code }} - {{ item.coupon.amount
          }}{{ item.coupon.unit }}
        </div>
        <v-icon v-else>mdi-circle-off-outline</v-icon>
      </template>

      <template v-slot:expanded-item="{ headers, item }">
        <td colspan="100%" class="pa-0">
          <v-list two-line flat>
            <template v-for="cartItem in item.items">
              <v-list-item :key="cartItem.id">
                <v-list-item-avatar tile size="70">
                  <v-img :src="cartItem.item.image" contain></v-img>
                </v-list-item-avatar>

                <v-list-item-content>
                  <v-list-item-subtitle>Item:</v-list-item-subtitle>
                  <v-list-item-title>{{
                    cartItem.item.name
                  }}</v-list-item-title>
                  <v-list-item-subtitle
                    >Quantity: {{ cartItem.quantity }}</v-list-item-subtitle
                  >
                </v-list-item-content>
                <v-list-item-action>
                  <v-list-item-subtitle>Price:</v-list-item-subtitle>
                  <v-list-item-title>{{
                    cartItem.final_price | currency
                  }}</v-list-item-title>
                </v-list-item-action>
              </v-list-item>
            </template>
          </v-list>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import Summary from "@/components/Checkout/Summary";
export default {
  components: { Summary },
  head() {
    return {
      title: "My Orders",
      meta: [
        {
          hid: "description",
          name: "description",
          content: "Completed Orders"
        }
      ]
    };
  },
  data() {
    return {
      expanded: [],
      headers: [
        { text: "Date", align: "left", value: "payment.timestamp" },
        { text: "Subtotal", value: "subtotal" },
        { text: "Coupon", value: "coupon" },
        { text: "Total", value: "total" }
      ]
    };
  },
  computed: {
    orders() {
      return this.$store.getters["profile/getOrders"];
    }
  },
  methods: {}
};
</script>

<style></style>
