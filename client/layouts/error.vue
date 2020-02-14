<template>
  <div class="container">
    <div>
      <template v-if="error.statusCode === 404">
        <h1>This page doesn't exist</h1>
        <p>The link may be broken or no longer exists.</p>
      </template>
      <div v-else>
        <h1>An error occurred</h1>
        <h2>{{ error }}</h2>
      </div>

      <nuxt-link to="/">Back to home page</nuxt-link>
    </div>
  </div>
</template>

<script>
export default {
  props: ["error"]
  // layout: "xyz" // you can set a custom layout for the error page
};
</script>
<style lang="scss" scoped>
.container {
  height: 100%;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  font-weight: 400;
  color: #666;
  h1 {
    text-transform: uppercase;
    font-weight: 700;
    font-size: 2.5rem;
    letter-spacing: -1px;
  }
  a {
    font-weight: 400;
    color: inherit;
  }
}
</style>
