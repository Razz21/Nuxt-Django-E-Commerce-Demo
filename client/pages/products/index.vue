<template>
  <v-container>
    <v-row>
      <v-col
        cols="12"
        md="4"
        :order="$vuetify.breakpoint.smAndDown ? '2' : '1'"
      >
        <div class="mb-8">
          <filter-input title="Colors" class="mt-4">
            <ColorFilter :colors="filterItems.colors" v-model="filters.color" />
          </filter-input>
          <filter-input title="Filter" class="mt-4">
            <LabelFilter
              :items="filterItems.materials"
              v-model="filters.material"
            />
          </filter-input>
          <filter-input title="Price" class="my-4">
            <div class="pt-8 px-4">
              <v-range-slider
                v-model="filters.price"
                hide-details
                min="0"
                :max="filterItems.max_price"
                thumb-label
                color="primary"
                track-color="grey"
              >
              </v-range-slider>
              <div class="d-flex justify-space-between">
                <div>0$</div>
                <div>{{ filterItems.max_price }}$</div>
              </div>
            </div>
          </filter-input>
          <v-btn block large color="primary" depressed @click="filter"
            >Filter</v-btn
          >
          <v-slide-x-transition>
            <v-btn
              v-show="filtersOn"
              @click="$router.replace({ query: null })"
              text
              depressed
              class="mt-6"
              color="error"
            >
              Clear Filters <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-slide-x-transition>
        </div>
        <v-divider class="my-8 mx-4"></v-divider>
        <CategoryList />
      </v-col>
      <v-col cols="12" md="8" order="1">
        <div class="d-flex justify-space-between align-end">
          <div class="body-2">{{ countItems }}</div>
          <OrderFilter :ordering="ordering" :order_types="order_types" />
        </div>

        <product-list :items="items" v-if="items.length">
          <template v-slot="{ item }">
            <FlippedCard :item="item" />
          </template>
        </product-list>
        <div
          v-else
          style="height:300px"
          class="d-flex justify-center align-center w-full text-center h-full"
        >
          <div class="display-1">
            No products were found matching your selection
          </div>
        </div>
        <Paginator :pagination="pagination" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import ProductCard from "@/components/Products/ProductCard";
import FlippedCard from "@/components/Products/ProductCard/FlippedCard";
import ProductList from "@/components/Products/ProductList";
import CategoryList from "@/components/Products/CategoryList";
import OrderFilter from "@/components/Products/ProductFilter/OrderFilter";
import Paginator from "@/components/Products/ProductFilter/Paginator";

import ColorFilter from "@/components/Products/ProductFilter/ColorFilter";
import LabelFilter from "@/components/Products/ProductFilter/LabelFilter";
import FilterInput from "@/components/Products/ProductFilter/FilterInput";
import { strip, parseQueryList, textRegex } from "@/utils";

function validateQuery(type, val, store) {
  const cb = {
    page: val => {
      return textRegex(val, /^[1-9]\d*$/);
    },
    ordering: val => {
      return val && store.getters["products/getOrdering"].includes(val);
    },
    color: val => {
      return textRegex(val, /^([1-9]\d*,?)+$/);
    },
    material: val => {
      return textRegex(val, /^([1-9]\d*,?)+$/);
    },
    price: val => {
      return textRegex(val, /^[0-9]\d*,[1-9]\d*$/);
    },
    search: val => {
      return textRegex(val, /^\w*$/i);
    }
  };
  return !!cb[type] && cb[type](val);
}

export default {
  components: {
    ProductCard,
    FlippedCard,
    ProductList,
    OrderFilter,
    CategoryList,
    Paginator,
    ColorFilter,
    LabelFilter,
    FilterInput
  },
  // scrollToTop: true,
  watchQuery: true,
  validate({ query, params, store }) {
    for (let [key, value] of Object.entries(query)) {
      if (!validateQuery(key, value, store)) {
        return false;
      }
    }
    if (params.slug) {
      return textRegex(params.slug, /^\w(-?\w)*$/);
    }
    return true;
  },
  head() {
    const category = this.$route.params.slug;
    const search = this.$route.query.search;
    return {
      title: category
        ? `Category ${category}`
        : search
        ? "Search results"
        : "All Products",
      meta: [
        {
          hid: "description",
          name: "description",
          content: "Product List"
        }
      ]
    };
  },
  async asyncData({ store, route, $axios }) {
    try {
      const data = await store.dispatch(
        "products/fetchProducts",
        route.fullPath
      );
      const { count, results, total_pages } = data;
      return {
        items: results,
        count,
        pagination: { total_pages, page: 1 }
      };
    } catch (err) {
      console.log(err);
    }
  },
  data() {
    return {
      ordering: "name",
      items: [],
      pagination: { total_pages: 1, page: 1 },
      count: 0,
      filters: {
        color: [],
        material: [],
        price: [0, 2000]
      },

      order_types: [
        { text: "Name &#8593;", value: "name" },
        { text: "Name &#8595;", value: "-name" },
        { text: "Price &#8593;", value: "order_price" },
        { text: "Price &#8595;", value: "-order_price" }
      ]
    };
  },
  watch: {
    pagination: {
      deep: true,
      handler(val, old) {
        if (val.page > 0 && val.page <= val.total_pages) {
          this.$router.push({
            query: { ...this.$route.query, page: val.page }
          });
        }
      }
    },
    ordering: {
      handler(val, old) {
        this.$router.push({
          query: { ...this.$route.query, ordering: val }
        });
      }
    },
    "$route.query": {
      immediate: true,
      handler(params) {
        this.initializeFilters();
        this.initializePage();
        // set filter/order values on param change
        for (let [key, value] of Object.entries(params)) {
          value && this.handleQueryParam(key, value);
        }
      }
    }
  },
  computed: {
    filterItems() {
      return this.$store.getters["products/getFilters"];
    },
    filtersOn() {
      return ["color", "price", "material"].some(f => f in this.$route.query);
    },
    countItems() {
      if (!this.count) {
        return "Products not found";
      } else {
        const { page, total_pages } = this.pagination;
        const pageSize = total_pages > 1 ? 9 : this.count;
        const min = pageSize * (page - 1) + 1;
        const rest =
          Math.floor(this.count / (pageSize * page)) > 0
            ? pageSize
            : this.count % (pageSize * (page - 1));
        const max = min + rest - 1;
        return `Showing ${min}-${max} of ${this.count} results`;
      }
    }
  },
  methods: {
    filter() {
      const filtered = Object.keys(this.filters)
        .filter(key => this.filters[key].length)
        .reduce((obj, key) => {
          return {
            ...obj,
            [key]: this.filters[key]
          };
        }, {});
      let query = new URLSearchParams(filtered).toString();
      console.log(query);
      this.$router.push(`?${query}`);
    },
    initializeFilters() {
      this.filters = {
        color: [],
        material: [],
        price: [0, 2000]
      };
    },
    initializePage() {
      this.pagination.page = 1;
      this.ordering = "name";
    },
    handleQueryParam(type, val) {
      const cb = {
        page: val => {
          this.pagination.page = parseInt(val);
        },
        ordering: val => {
          this.ordering = val;
        },
        color: val => {
          this.filters.color = parseQueryList(val);
        },
        material: val => {
          this.filters.material = parseQueryList(val);
        },
        price: val => {
          this.filters.price = parseQueryList(val).sort((a, b) => a > b);
        }
      };
      return !!cb[type] && cb[type](val);
    }
  }
};
</script>

<style></style>
