<template>
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
</template>

<script>
export default {
  data() {
    return {
      card: undefined
    };
  },
  mounted() {
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

    // Add an instance of the card Element into the `card-element` <div>.
    this.card.mount(this.$refs.card);

    //todo form validation
    this.card.addEventListener("change", function(event) {
      var displayError = document.getElementById("card-errors");
      if (event.error) {
        displayError.textContent = event.error.message;
      } else {
        displayError.textContent = "";
      }
    });
  }
};
</script>

<style scoped lang="scss">
#payment-form {
  width: 100%;
}
.StripeElement {
  box-sizing: border-box;

  height: 40px;

  padding: 10px 12px;

  border: 1px solid transparent;
  border-radius: 4px;
  background-color: white;

  box-shadow: 0 1px 3px 0 #e6ebf1;
  -webkit-transition: box-shadow 150ms ease;
  transition: box-shadow 150ms ease;
}

.StripeElement--focus {
  box-shadow: 0 1px 3px 0 #cfd7df;
}

.StripeElement--invalid {
  border-color: #fa755a;
}

.StripeElement--webkit-autofill {
  background-color: #fefde5 !important;
}
</style>
