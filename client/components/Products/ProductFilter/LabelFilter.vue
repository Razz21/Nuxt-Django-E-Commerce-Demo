<template>
  <v-list color="transparent" dense>
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title>Materials</v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-list-item-group
      :value="value"
      @change="$emit('input', $event)"
      multiple
      color="primary"
      class="ml-10"
    >
      <v-list-item v-for="item in items" :key="item.id" :value="item.id">
        <template v-slot:default="{ active, toggle }">
          <v-list-item-content>
            <v-list-item-title
              v-text="item.name"
              class="text-capitalize"
            ></v-list-item-title>
          </v-list-item-content>
          <v-list-item-action class="my-1">
            <v-checkbox
              hide-details
              :true-value="item.id"
              :input-value="active"
              @click="toggle"
              color="primary"
            ></v-checkbox>
          </v-list-item-action>
        </template>
      </v-list-item>
    </v-list-item-group>
  </v-list>
</template>

<script>
export default {
  props: {
    items: Array,
    value: Array
  }
};
</script>

<style></style>
