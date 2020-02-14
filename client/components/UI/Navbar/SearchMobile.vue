<template>
  <search-wrap>
    <template
      v-slot="{ results, inputProps, inputEvents, loading, input, clear }"
    >
      <div class="w-full" v-click-outside="clear">
        <div class="d-flex align-center w-full white">
          <v-btn icon @click="$emit('toggle-search')">
            <v-icon>mdi-arrow-left</v-icon>
          </v-btn>
          <v-text-field
            v-bind="inputProps"
            v-on="inputEvents"
            autofocus
            full-width
            hide-details
            solo
            flat
            label="Search"
            color="primary"
          >
            <template v-slot:append>
              <v-fade-transition leave-absolute>
                <v-progress-circular
                  v-if="loading"
                  size="24"
                  color="info"
                  indeterminate
                ></v-progress-circular>
                <v-icon v-else color="primary">
                  mdi-magnify
                </v-icon>
              </v-fade-transition>
            </template>
          </v-text-field>
        </div>

        <Results :data="results" :input="input" ref="results" />
      </div>
    </template>
  </search-wrap>
</template>

<script>
import SearchWrap from "./SearchWrap";
import Results from "./Results";
export default {
  components: { Results, SearchWrap },
  data() {
    return {};
  }
};
</script>

<style scoped lang="scss"></style>
