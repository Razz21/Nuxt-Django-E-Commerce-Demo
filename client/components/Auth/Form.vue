<template>
  <v-card
    raised
    class="d-flex flex-column auth-card light-white mx-auto justify-center"
    width="100%"
    height="100%"
  >
    <v-card-title
      class="justify-center align-end jusify-self-end font-weight-medium display-1 text-capitalize"
      >{{ title }}
    </v-card-title>

    <v-card-text class="py-0">
      <v-alert
        dense
        :type="alert.type || 'error'"
        v-if="alert && alert.detail"
        transition="scale-transition"
      >
        {{ alert.detail }}
      </v-alert>
    </v-card-text>
    <v-card-text>
      <slot />
    </v-card-text>

    <v-divider></v-divider>
    <v-card-actions
      class="gray--text justify-center font-weight-regular py-5 subtitle-2"
    >
      <slot name="actions" />
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  props: {
    title: String,
    alert: Object
  }
};
</script>

<style></style>
