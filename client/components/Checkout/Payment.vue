<template>
  <div>
    <v-item-group
      activeClass="activeItem"
      class="w-full"
      v-model="paymentMethod"
      mandatory
    >
      <v-row>
        <v-col cols="6">
          <v-item v-slot:default="{ active, toggle }">
            <v-card @click="toggle" outlined class="text-center">
              <v-card-text class="pa-3">
                <v-icon x-large>mdi-credit-card-outline</v-icon>
                Credit Card</v-card-text
              >
            </v-card>
          </v-item>
        </v-col>
        <v-col cols="6">
          <v-item v-slot:default="{ active, toggle }">
            <v-card @click="toggle" outlined class="text-center" style="flex:1">
              <v-card-text class="pa-3"
                ><v-icon x-large>mdi-paypal</v-icon>Paypal</v-card-text
              >
            </v-card>
          </v-item>
        </v-col>
      </v-row>
    </v-item-group>
    <!-- <CardForm /> -->
  </div>
</template>

<script>
import CardForm from "@/components/Checkout/CardForm";
export default {
  components: { CardForm },
  data() {
    return {
      paymentMethod: 0
    };
  }
};
</script>

<style scoped>
.activeItem {
  background-color: #f1f1f1;
}
</style>
