<template>
  <div class="results shadow-lg" ref="list" :style="{ '--height': height }">
    <template v-if="data">
      <template v-if="data.results.length">
        <v-subheader
          >Showing {{ data.results.length }} of total {{ data.count }}
          {{ "result" | pluralize(data.results.length) }}</v-subheader
        >

        <v-list two-line flat style="background:transparent">
          <template v-for="(result, idx) in data.results">
            <v-list-item
              :to="{ name: 'products-slug', params: { slug: result.slug } }"
              :key="result.id"
              class="result-item"
              :style="{ '--i': idx }"
            >
              <v-list-item-avatar tile size="70">
                <v-img :src="result.image" contain></v-img>
              </v-list-item-avatar>

              <v-list-item-content>
                <v-list-item-title>{{ result.name }}</v-list-item-title>
                <v-list-item-subtitle>{{
                  resultCategories(result.category)
                }}</v-list-item-subtitle>
              </v-list-item-content>

              <v-list-item-action class="body-1 justify-center">
                <div class="caption">Price:</div>
                <template v-if="result.discount">
                  <span>
                    {{ result.discount | currency }}
                  </span>
                  <span style="text-decoration:line-through" class="grey--text">
                    {{ result.price | currency }}
                  </span>
                </template>
                <span v-else>{{ result.price | currency }}</span>
              </v-list-item-action>
            </v-list-item>
            <v-divider
              :key="result.id + 'd'"
              v-if="idx < countResults - 1"
            ></v-divider>
          </template>
        </v-list>
        <v-divider></v-divider>
        <v-btn
          @click="moreResults"
          block
          tile
          depressed
          color="primary"
          v-if="countResults"
          >Show all results</v-btn
        >
      </template>
      <template v-else>
        <v-subheader>Not found any results for "{{ input }}"</v-subheader>
      </template>
    </template>
  </div>
</template>

<script>
export default {
  inject: ["clear"],
  props: {
    data: Object,
    input: { type: String, default: "" }
  },
  data() {
    return {
      height: 0
    };
  },
  watch: {
    data(val) {
      this.$nextTick(() => {
        this.height = this.$refs.list.getBoundingClientRect().height;
      });
    }
  },
  computed: {
    countAll() {
      return this.data.count;
    },
    countResults() {
      return this.data.results.length;
    }
  },
  methods: {
    moreResults() {
      this.$router.push({ name: "products", query: { search: this.input } });
      this.clear();
    },
    orderPrice(item) {
      return item.discount_price || item.price;
    },
    resultCategories(item) {
      const categories = item.map(i => i.name);
      return categories.join("/");
    }
  }
};
</script>

<style lang="scss" scoped>
.results {
  --color-border: #eaeced;
  --border-radius: 0.5rem;
  position: fixed;
  top: 100%;
  left: 0;
  max-height: 100vh;
  min-width: 270px;
  width: 100%;
  z-index: -1;
  font-size: 0.6em;
  // border-bottom-left-radius: var(--border-radius);
  // border-bottom-right-radius: var(--border-radius);
  margin: 0 0;
  padding: 0;
  list-style-type: none;
  @include breakpoint(sm) {
    position: absolute;
    max-width: 400px;
  }

  &:before {
    z-index: -1;
    content: "";
    position: absolute;
    top: calc(var(--border-radius) * -1);
    left: 0;
    width: 100%;
    background-color: #f7f9fb;

    height: calc((var(--height, 0) * 1px));
    transition: height 0.5s;
    border-radius: inherit;
  }
}

.result-item {
  margin: 0.25rem 0.5em;
  padding: 0.5em 0.6em;
  list-style-type: none;
  border-radius: 0.5rem;
  animation: pop-in 0.3s backwards;
  animation-delay: calc(var(--i) * 0.08s);
  background-color: transparent;
  transition: all 0.1s;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  color: #333;

  // &:before {
  //   content: "dog";
  //   text-transform: uppercase;
  //   font-size: 0.5rem;
  //   font-weight: bold;
  //   background: #6d7386;
  //   color: white;
  //   border-radius: 0.25em;
  //   margin-right: 0.5rem;
  //   display: inline-block;
  //   padding: 0.25em;
  // }

  &:hover {
    background-color: #edeff2;
    cursor: pointer;
  }

  @keyframes pop-in {
    from {
      transform: scale(0.8);
      opacity: 0;
    }
  }
}
</style>
