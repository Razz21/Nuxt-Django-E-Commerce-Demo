<template>
  <div>
    <v-item-group
      multiple
      :value="value"
      @change="$emit('input', $event)"
      class="colors"
    >
      <v-item
        v-slot:default="{ active, toggle }"
        v-for="(color, idx) in colors"
        :key="idx"
        :value="color.id"
      >
        <ColorCheckbox
          :color="color"
          :checked="active"
          @change.native="toggle"
        />
      </v-item>
    </v-item-group>
  </div>
</template>

<script>
import ColorCheckbox from "./ColorCheckbox";
export default {
  components: { ColorCheckbox },
  props: ["colors", "value"],
  data() {
    return {};
  }
};
</script>

<style lang="scss">
.colors {
  flex-flow: row wrap;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  > label {
    flex: 0 1 20%;
    min-width: 50px;
    margin: 0 0.5rem 2rem 0;
  }
}
</style>
