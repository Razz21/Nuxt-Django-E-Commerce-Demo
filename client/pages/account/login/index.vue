<router>
  {
    name:'login',
    path: '/login/'
  }
</router>
<script>
export default {
  middleware: ["show-modal"],
  auth: "guest",
  meta: {
    modal: true
  }
};
</script>
