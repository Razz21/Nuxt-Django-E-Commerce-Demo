<template>
  <v-container data-state="IDLE" id="wrapper">
    <div data-scene="progress" class="screen text-center">
      <transition-group name="progress" style="max-width:600px">
        <v-progress-circular
          key="prog"
          :color="
            currentState === 'SUCCESS'
              ? 'success'
              : currentState === 'ERROR'
              ? 'error'
              : ''
          "
          size="100"
          :indeterminate="currentState === 'LOADING'"
          width="3"
          value="100"
        >
          <v-scale-transition origin="center center">
            <v-icon v-if="currentState === 'SUCCESS'" color="success" size="96"
              >mdi-check</v-icon
            >
            <v-icon v-if="currentState === 'ERROR'" color="error" size="96"
              >mdi-exclamation</v-icon
            >
          </v-scale-transition>
        </v-progress-circular>
        <div v-if="currentState === 'ERROR'" key="2">
          <div class="headline mt-5">
            Some error occured. Check, if you provided all required data and try
            again.
          </div>
          <v-btn @click="send('click')" depressed color="error">Back</v-btn>
        </div>
        <div v-if="currentState === 'SUCCESS'" key="1" class="mt-5">
          <div class="headline ">
            Payment successful!
          </div>
          <div></div>
          <nuxt-link to="/">Back to home page</nuxt-link>
        </div>
      </transition-group>
    </div>

    <div data-scene="form" class="screen">
      <v-btn text color="primary">
        <v-icon>mdi-chevron-left</v-icon>
        Back
      </v-btn>
      <v-form @submit.prevent="validate" ref="form" v-model="valid">
        <v-row>
          <v-col
            cols="12"
            md="7"
            :order="$vuetify.breakpoint.smAndDown ? 1 : -1"
          >
            <div>
              <h4 class="body-2 my-3">Payment Method</h4>
              <v-card class="shadow-md">
                <v-card-text>
                  <Payment />
                  <form
                    action="/charge"
                    method="post"
                    id="payment-form"
                    @submit.prevent="submit"
                  >
                    <div class="form-row">
                      <label for="card-element">
                        Credit or debit card
                      </label>
                      <div ref="card">
                        <!-- A Stripe Element will be inserted here. -->
                      </div>

                      <!-- Used to display form errors. -->
                      <div id="card-errors" role="alert"></div>
                    </div>
                  </form>
                </v-card-text>
              </v-card>
            </div>
            <div class="mt-8">
              <h4 class="body-2 my-3">Shipping Address</h4>
              <v-card class="shadow-md">
                <v-card-text>
                  <Address :address.sync="shipping" :valid="valid" />
                </v-card-text>
              </v-card>
            </div>

            <div class="mt-8">
              <h4 class="body-2 my-3">Billing Address</h4>

              <v-card class="shadow-md">
                <v-radio-group
                  v-model="radioGroup"
                  hide-details
                  :rules="[v => !!v || 'This field is required']"
                >
                  <v-list-item>
                    <v-radio
                      label="Same as shipping address"
                      :value="1"
                    ></v-radio>
                  </v-list-item>
                  <v-divider></v-divider>
                  <v-list-item>
                    <v-radio
                      label="Use a different billing address"
                      :value="2"
                    ></v-radio>
                  </v-list-item>
                </v-radio-group>
                <v-card-text v-if="radioGroup === 2">
                  <Address :address.sync="billing" :valid="valid" />
                </v-card-text>
              </v-card>
            </div>
          </v-col>
          <v-col cols="12" md="5">
            <Summary :cart="cart" />
          </v-col>
        </v-row>
      </v-form>
      <div class="my-8 d-flex justify-center">
        <v-btn x-large color="primary" dark @click="validate"
          >Place your order</v-btn
        >
      </div>
    </div>
  </v-container>
</template>

<script>
const machine = {
  initial: "LOADING",
  states: {
    IDLE: {
      on: {
        submit: "LOADING"
      }
    },
    LOADING: {
      on: {
        success: "SUCCESS",
        error: "ERROR"
      }
    },
    ERROR: {
      on: {
        click: "IDLE"
      }
    },
    SUCCESS: {
      on: {}
    }
  }
};

import Payment from "@/components/Checkout/Payment";
import Summary from "@/components/Checkout/Summary";
import Address from "@/components/Checkout/Address";
export default {
  middleware: ["auth", "checkout"],
  components: { Summary, Payment, Address },
  head() {
    return {
      title: "Checkout",
      meta: [
        {
          hid: "description",
          name: "description",
          content: "Checkout order"
        }
      ]
    };
  },
  fetch({ store }) {
    store.dispatch("checkout/initData");
  },
  data() {
    return {
      valid: true,
      radioGroup: undefined,
      shipping: null,
      billing: null,
      stripeToken: "",
      stripe: "",
      card: "",
      status: false,
      app: undefined,
      currentState: machine.initial
    };
  },
  computed: {
    cart() {
      return this.$store.getters["cart/getCart"];
    },
    addresses() {
      return this.$store.getters["profile/getAddresses"];
    }
  },
  methods: {
    validate() {
      if (this.$refs.form.validate()) {
        this.submit();
      }
    },
    submit() {
      // fixme validate input before createToken
      this.stripe
        .createToken(this.card)
        .then(res => {
          if (res.error) {
            console.log(res.error);
            // this.send("error");
            return;
          }
          console.log({
            stripeToken: res.token.id,
            shipping_id: this.shipping.id,
            billing_id: this.billing.id
          });
          this.send("submit");
          this.$store
            .dispatch("cart/checkout", {
              stripeToken: res.token.id,
              shipping_id: this.shipping.id,
              billing_id: this.billing.id
            })
            .then(res => {
              console.log("payment ", res);
              this.send("success");
            })
            .catch(err => {
              console.log(err);
              this.send("error");
            });
        })
        .catch(err => {
          this.send("error");
          console.log(err.message);
        });
    },
    includeStripe(URL, callback) {
      let documentTag = document,
        tag = "script",
        object = documentTag.createElement(tag),
        scriptTag = documentTag.getElementsByTagName(tag)[0];
      object.src = "https://" + URL;
      // object.setAttribute("defer", "defer");
      if (callback) {
        object.addEventListener(
          "load",
          function(e) {
            callback(null, e);
          },
          false
        );
      }

      scriptTag.parentNode.insertBefore(object, scriptTag);
    },
    configureStripe() {
      this.stripe = Stripe(process.env.STRIPE_PUBLIC_KEY);
      const elements = this.stripe.elements();
      const style = {
        base: {
          color: "#32325d",
          fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
          fontSmoothing: "antialiased",
          fontSize: "16px",
          "::placeholder": {
            color: "#aab7c4"
          }
        },
        invalid: {
          color: "#fa755a",
          iconColor: "#fa755a"
        }
      };
      this.card = elements.create("card", { style: style });
      this.card.mount(this.$refs.card);

      this.card.addEventListener("change", function(event) {
        var displayError = document.getElementById("card-errors");
        if (event.error) {
          displayError.textContent = event.error.message;
        } else {
          displayError.textContent = "";
        }
      });
    },
    transition(state, event) {
      return machine.states[state].on[event] || state;
    },
    send(event) {
      this.currentState = this.transition(this.currentState, event);
      this.app.setAttribute("data-state", this.currentState);
    }
  },
  watch: {
    radioGroup(val) {
      if (val === 1) {
        this.billing = this.shipping;
      } else {
        this.billing = null;
      }
    },
    shipping(val) {
      if (val && this.radioGroup === 1) {
        this.billing = val;
      }
    }
  },
  mounted() {
    this.includeStripe("js.stripe.com/v3/", () => {
      this.configureStripe();
    });
    this.app = document.getElementById("wrapper");
  }
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
