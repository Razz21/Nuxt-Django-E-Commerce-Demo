<template>
  <v-card
    color="transparent"
    width="100%"
    height="100%"
    class="item "
    flat
    nuxt
    :to="{ name: 'products-slug', params: { slug: item.slug } }"
  >
    <div>
      <div class="item-img">
        <div
          class="item-img-bg shadow-md"
          :style="`background-color:${item.color}30`"
        ></div>
        <v-img
          class="shadowed"
          width="100%"
          height="200px"
          :src="item.image"
          contain
        >
        </v-img>
      </div>
      <div
        class="h-full text-capitalize mt-n8 item-content"
        :class="[isMobile ? 'px-2' : ' px-4']"
      >
        <v-card class="shadow-lg pa-3">
          <Label v-if="item.label" :name="item.label" />
          <h1 class="black--text subtitle-1 font-weight-medium ">
            {{ item.name }}
          </h1>
          <div class="d-flex ">
            <template v-if="item.discount_price">
              <h2
                class="subtitle-2 font-weight-medium grey--text"
                style="text-decoration:line-through"
              >
                {{ item.price | currency }}
              </h2>
              <h2 class="subtitle-2 font-weight-medium carbon--text">
                {{ item.discount_price | currency }}
              </h2>
            </template>
            <h2 v-else class="subtitle-2 font-weight-medium carbon--text">
              {{ item.price | currency }}
            </h2>
          </div>
        </v-card>
      </div>
    </div>
  </v-card>
</template>

<script>
import { Flipped } from "vue-flip-toolkit";
import Label from "./Label";
export default {
  components: { Flipped, Label },
  props: { item: Object },
  methods: {
    handleClick() {
      // const item = this.item;
      // this.$emit("select", item);
      this.$router.push({
        name: "products-slug",
        params: { slug: this.item.slug }
      });
    }
  }
};
</script>

<style lang="scss" scoped>
@import "./style.scss";
</style>
