<template>
  <v-footer padless style="bottom:0;">
    <v-container>
      <v-card flat tile color="transparent" class="white--text text-center">
        <v-card-text>
          <div
            class="title font-weight-black page-title"
            style="transform-origin:center center"
          >
            TAKT
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-text> &copy; {{ new Date().getFullYear() }} </v-card-text>
      </v-card>
    </v-container>
  </v-footer>
</template>

<script>
export default {};
</script>

<style></style>
