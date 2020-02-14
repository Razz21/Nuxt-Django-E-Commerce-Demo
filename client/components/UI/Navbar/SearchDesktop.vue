<template>
  <search-wrap>
    <template
      v-slot="{ results, inputProps, inputEvents, loading, clear, input }"
    >
      <div v-click-outside="clear">
        <v-text-field
          v-bind="inputProps"
          v-on="inputEvents"
          style="min-width:0"
          background-color="#eeeeee"
          flat
          solo
          rounded
          dense
          hide-details
          label="Search"
        >
          <template v-slot:append>
            <v-fade-transition leave-absolute>
              <v-progress-circular
                v-if="loading"
                size="24"
                color="info"
                indeterminate
              ></v-progress-circular>
            </v-fade-transition>
          </template>
        </v-text-field>

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

<style scoped lang="scss">
.v-input__append-inner {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
