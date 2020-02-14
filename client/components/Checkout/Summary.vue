<template>
  <div>
    <div class="text-capitalize body-2 mb-3">
      Order Summary
    </div>

    <v-expansion-panels focusable v-model="order">
      <v-expansion-panel class="shadow-md">
        <v-expansion-panel-header class="px-4 py-1">
          <template v-slot:default="{ open }">
            <v-fade-transition leave-absolute>
              <span v-if="open" key="0" class="body-1"
                >Close order Summary</span
              >
              <span v-else key="1">
                <v-list-item class="d-flex px-0">
                  <v-badge
                    :content="cart.items.length"
                    :value="cart.items.length"
                    bordered
                    color="green"
                    overlap
                    class="mr-2"
                  >
                    <v-icon>mdi-shopping</v-icon>
                  </v-badge>
                  <div class="body-1 flex-grow-1">Show order summary</div>
                  <div class="body-1">{{ cart.total | currency }}</div>
                </v-list-item>
              </span>
            </v-fade-transition>
          </template>
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-list two-line>
            <template v-for="cartItem in cart.items">
              <v-list-item :key="cartItem.id" class="px-0">
                <v-list-item-avatar tile size="70">
                  <v-img :src="cartItem.item.image" contain></v-img>
                </v-list-item-avatar>

                <v-list-item-content>
                  <v-list-item-title>{{
                    cartItem.item.name
                  }}</v-list-item-title>
                  <v-list-item-subtitle
                    >Quantity: {{ cartItem.quantity }}</v-list-item-subtitle
                  >
                </v-list-item-content>
                <v-list-item-action>
                  <v-list-item-title>{{
                    cartItem.final_price | currency
                  }}</v-list-item-title>
                </v-list-item-action>
              </v-list-item>
              <v-divider :key="cartItem.id + 'd'"></v-divider>
            </template>
          </v-list>

          <div
            class="d-flex justify-space-between align-baseline"
            v-if="cart.coupon"
          >
            <div class="subtitle-2 text-capitalize">Subtotal:</div>
            <div class="subtitle-2">{{ cart.subtotal | currency }}</div>
          </div>
          <div
            class="d-flex justify-space-between align-baseline"
            v-if="cart.coupon"
          >
            <div class="subtitle-2 text-capitalize">
              {{ cart.coupon.code }}
            </div>
            <div class="subtitle-2">
              &#45;{{ cart.coupon.amount }}{{ cart.coupon.unit }}
            </div>
          </div>
          <v-divider class="my-2"></v-divider>
          <div class="d-flex justify-space-between align-baseline">
            <div class="title text-capitalize">Total:</div>
            <div class="title">{{ cart.total | currency }}</div>
          </div>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>

    <div class="mt-8">
      <v-fade-transition mode="out-in">
        <v-form
          v-if="couponForm"
          ref="form"
          @submit.prevent="validate"
          class="d-flex "
          lazy-validation
          v-model="form"
        >
          <v-text-field
            validate-on-blur
            autofocus
            v-model="coupon"
            :rules="[v => !!v || 'Please paste valid code.']"
            single-line
            hide-details
            dense
            label="Discount Code"
            class="mr-2"
            outlined
            color="primary"
            prepend-icon="mdi-close-circle"
            @click:prepend="couponForm = false"
          ></v-text-field>
          <v-btn
            color="primary"
            dark
            depressed
            style="height:inherit"
            type="submit"
            :loading="loading === 1"
            >Apply</v-btn
          >
        </v-form>
        <v-btn
          v-else
          @click="couponForm = true"
          outlined
          block
          color="primary"
          small
          style="height:40px"
          >Have a discount code? Click to enter it.</v-btn
        >
      </v-fade-transition>
    </div>
  </div>
</template>

<script>
// todo discount-code
export default {
  props: ["cart"],
  data() {
    return {
      order: 0,
      form: true,
      couponForm: false,
      coupon: ""
    };
  },
  computed: {
    loading() {
      return this.$store.getters["cart/getLoading"];
    }
  },
  watch: {
    "$vuetify.breakpoint.smAndDown"(val) {
      this.order = val ? null : 0;
    }
  },
  methods: {
    validate() {
      if (this.$refs.form.validate()) {
        this.$store
          .dispatch("cart/addCoupon", { code: this.coupon })
          .then(() => {
            this.$refs.form.reset();
            this.couponForm = false;
          });
      }
    }
  },
  mounted() {
    if (this.$vuetify.breakpoint.smAndDown) {
      this.order = null;
    }
  }
};
</script>

<style scoped lang="scss">
.v-expansion-panel::before {
  @extend .shadow-md;
}
</style>
