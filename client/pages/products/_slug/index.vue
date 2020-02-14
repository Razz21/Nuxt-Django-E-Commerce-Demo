<template>
  <v-container class="pt-0 ">
    <section id="head" class="d-flex flex-column ">
      <div class="flip_detail flex-grow-1">
        <v-btn
          text
          @click="goBack"
          style="z-index:1;top:10px;left:10px"
          color="grey--text"
          class="align-self-start"
        >
          <v-icon>mdi-arrow-left</v-icon>
          Return
        </v-btn>
        <Flipped :flip-id="item.slug">
          <div
            class="item-bg"
            :style="`background-color:${item.color}30`"
          ></div>
        </Flipped>

        <!-- <v-container class="h-full"> -->
        <v-row
          class="h-full mx-0 flex-nowrap "
          justify="center"
          align="center"
          :class="{ 'flex-column': isMobile }"
        >
          <v-col v-bind="colProps">
            <div class="d-flex justify-center align-center ">
              <div class="img-bg"></div>

              <v-carousel height="auto" hide-delimiter-background>
                <Flipped :flip-id="item.slug + 'img'">
                  <v-carousel-item>
                    <v-img
                      :src="item.images[0].path"
                      aspect-ratio="1"
                      contain
                    ></v-img>
                  </v-carousel-item>
                </Flipped>
                <template v-if="moreImages.length">
                  <v-carousel-item
                    v-for="(img, i) in moreImages"
                    :key="i"
                    :src="img.path"
                  ></v-carousel-item>
                </template>
              </v-carousel>
            </div>
          </v-col>
          <v-col v-bind="colProps">
            <div class="relative item-body d-grid">
              <div class="mb-3">
                <div class="display-2 font-weight-medium">
                  {{ item.name }}
                </div>
                <div class="display-1 font-weight-regular item-categories">
                  <template v-for="(c, index) in item.category">
                    <nuxt-link
                      :to="{
                        name: 'products-category',
                        params: { slug: c.slug }
                      }"
                      :key="c.id"
                      >{{ c.name }}</nuxt-link
                    >
                    <div
                      :key="c.id + 'div'"
                      v-if="index + 1 < item.category.length"
                    >
                      /
                    </div>
                  </template>
                </div>

                <div class="display-1 mt-8 primary--text">
                  {{ item.price | currency }}
                </div>
              </div>
              <div class="d-flex justify-space-between">
                <div>
                  <div>
                    <v-subheader class="pl-0">Materials</v-subheader>
                    <div class="body-2 font-weight-regular">
                      {{ materials(item.material) }}
                    </div>
                  </div>
                  <div>
                    <v-subheader class="pl-0">Colors</v-subheader>
                    <div
                      :style="{ backgroundColor: item.color }"
                      style="height:30px;width:30px; border-radius:50%"
                    ></div>
                  </div>
                </div>
                <v-btn
                  tile
                  class="add-to-cart"
                  color="primary"
                  style=""
                  dark
                  @click="addToCart(item.slug)"
                  >Add <v-icon small>mdi-plus</v-icon></v-btn
                >
              </div>
            </div>
          </v-col>
        </v-row>
        <!-- </v-container> -->
      </div>

      <v-row justify="end" class="bottom-0 flex-grow-0">
        <v-col cols="12" sm="6" class="py-0">
          <div
            @click="$vuetify.goTo('#details')"
            class="d-flex justify-space-between px-10 py-6 primary-light align-baseline caption cursor-pointer"
          >
            <p
              class="text-uppercase font-weight-medium grey--text text--darken-2 ma-0"
            >
              Product Details
            </p>
            <span class="font-weight-light title">&#8595;</span>
          </div>
        </v-col>
      </v-row>
    </section>
    <section class="my-8" id="details">
      <v-tabs class="shadow">
        <v-tab>Description</v-tab>

        <v-tab-item>
          <v-container>
            {{ item.description }}
          </v-container>
        </v-tab-item>
      </v-tabs>
      <!-- <p class="body-2 mt-8">
        </p> -->
    </section>
  </v-container>
</template>

<script>
import { textRegex } from "@/utils";
import { Flipper, Flipped } from "vue-flip-toolkit";
export default {
  name: "products-slug",
  transition: { mode: "in-out" },
  components: { Flipped },
  scrollToTop: true,
  validate({ params }) {
    return textRegex(params.slug, /^\w(-?\w)*$/);
  },
  head() {
    return {
      title: this.item.name,
      meta: [
        {
          hid: "description",
          name: "description",
          content: "Product detail Information"
        }
      ]
    };
  },
  async asyncData({ store, params, error, from }) {
    try {
      let item = await store.dispatch("products/fetchDetail", params.slug);
      return { item, from };
    } catch (err) {
      console.log("err", err.response.data);
      // todo 404 redirect
      if (err.response.status === 404) {
        error({ statusCode: 404, message: "Item not found" });
      }
    }
  },
  data() {
    return {};
  },
  computed: {
    colProps() {
      return this.isMobile ? {} : { cols: "6" };
    },
    moreImages() {
      return this.item.images.slice(1);
    }
  },
  methods: {
    materials(arr) {
      return arr.join("/ ");
    },
    addToCart(slug) {
      this.$store.dispatch("cart/addToCart", { slug });
    },
    goBack() {
      let path = "/";
      if (this.from) {
        path = this.from.fullPath;
      }
      this.$router.push(path);
    }
  }
};
</script>

<style lang="scss">
@import "./style.scss";
</style>
