<template>
  <div class="primary-light w-full brick">
    <v-container class="white-color">
      <section
        id="hero"
        class="w-full d-flex overflow-hidden"
        style="height:500px;"
      >
        <v-img
          :src="heroImg"
          width="100%"
          height="100%"
          position="right bottom"
          contain
        >
          <div
            class="flex-grow-1 d-flex align-center h-full"
            style="padding-left:10%"
          >
            <div
              class="text-text-uppercase font-weight-medium "
              :class="[isMobile ? 'display-2' : 'display-3']"
            >
              <p>Style<br />Comfort &#38;<br />Affortable</p>
              <v-btn
                x-large
                dark
                tile
                depressed
                color="primary"
                class="body-1 text-capitalize"
                :to="{ name: 'products' }"
                >Explore all items</v-btn
              >
            </div>
          </div>
        </v-img>
      </section>

      <section id="collections">
        <v-row v-for="item in collections" :key="item.title">
          <v-col cols="4">
            <v-img
              class="image"
              aspect-ratio="1"
              height="100%"
              :src="item.image"
            ></v-img>
          </v-col>
          <v-col cols="8">
            <div class="h-full w-full d-flex align-center description">
              <div>
                <h1 :class="[isMobile ? 'title' : 'display-1']">
                  {{ item.title }}
                </h1>
                <h2 :class="[isMobile ? 'subtitle-1' : 'title']">
                  {{ item.subtitle }}
                </h2>
                <v-btn
                  depressed
                  dark
                  color="primary"
                  nuxt
                  :to="item.link"
                  class="text-capitalize"
                  :class="[isMobile ? 'caption' : 'body-2']"
                  >View Collection</v-btn
                >
              </div>
            </div>
          </v-col>
        </v-row>
      </section>

      <section id="latest" class="mt-12">
        <div class="display-1 text-center text-capitalize">
          Our Latest Products
        </div>
        <v-slide-group show-arrows class="py-2">
          <v-slide-item v-for="item in latestProducts" :key="item.id">
            <v-card flat width="200" class="ma-4">
              <ProductCard :item="item" />
            </v-card>
          </v-slide-item>
        </v-slide-group>
      </section>
      <section
        id="contact"
        class="my-12 white--text d-flex flex-column align-center justify-center"
      >
        <h1 class="headline text-capitalize">Connect with Us:</h1>
        <div class="mt-3">
          <v-btn
            v-for="item in linkItems"
            :key="item.icon"
            class="mx-4 white--text"
            dark
            icon
            large
            :href="item.link"
            target="_blank"
          >
            <v-icon size="24px">{{ item.icon }}</v-icon>
          </v-btn>
        </div>
      </section>
    </v-container>
  </div>
</template>

<script>
import ProductCard from "@/components/Products/ProductCard";
export default {
  head() {
    return {
      title: "Home",
      meta: [
        {
          hid: "description",
          name: "description",
          content: "Home page"
        }
      ]
    };
  },
  scrollToTop: true,
  components: { ProductCard },
  data() {
    return {
      collections: [
        {
          title: "Chair Collection",
          subtitle: "New collection",
          image: require("~/assets/images/C2.jpg"),
          link: { name: "products-category", params: { slug: "chair" } }
        },
        {
          title: "Tables Collection",
          subtitle: "New collection",
          image: require("~/assets/images/B2.jpg"),
          link: { name: "products-category", params: { slug: "table" } }
        },
        {
          title: "Shelves Collection",
          subtitle: "New collection",
          image: require("~/assets/images/D1.jpg"),
          link: { name: "products-category", params: { slug: "shelf" } }
        }
      ],
      linkItems: [
        { icon: "mdi-facebook", link: "http://www.facebook.com" },
        { icon: "mdi-twitter", link: "http://www.twitter.com" },
        { icon: "mdi-linkedin", link: "http://www.linkedin.com" },
        { icon: "mdi-instagram", link: "http://www.instagram.com" }
      ]
    };
  },
  computed: {
    cart() {
      return this.$store.getters["cart/getCart"];
    },
    products() {
      return this.$store.getters["products/getProducts"];
    },
    heroImg() {
      return require("~/assets/images/image1.png");
    },
    latestProducts() {
      return this.$store.getters["products/getLatest"];
    }
  },
  methods: {},
  mounted() {}
};
</script>

<style lang="scss">
section {
  &#hero {
    // background: linear-gradient(90deg, #fff0 30%, #b6b1ab 100%);
    background-color: #b6b1ab;
  }
  &#collections {
    .row {
      min-height: 150px;

      &:nth-child(even) {
        flex-direction: row-reverse;
      }
      .col {
        max-height: 300px;
      }

      &:not(:last-child) {
        > .col {
          padding-bottom: 0;
        }
      }
    }

    .description {
      padding-left: 12px;
      background-repeat: repeat;
      background-color: #fff;
      background-color: $gray;
      background-image: url("https://www.transparenttextures.com/patterns/diagonal-striped-brick.png");

      @include breakpoint(sm) {
        padding-left: 48px;
      }
      @include breakpoint(md) {
        padding-left: 96px;
      }
    }
  }
  &#contact {
    height: 200px;
    background-image: url("../assets/images/contact.jpg");
    background-position: center center;
    background-repeat: no-repeat;
    background-size: cover;
    &::before {
      content: "";
      position: absolute;
      width: 100%;
      height: 100%;
      background: #000;
      opacity: 0.75;
    }
    h1::after {
      content: "";
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      border-bottom: 3px solid $primary;
    }
    a:hover {
      color: $primary !important;
    }
  }
}
</style>
