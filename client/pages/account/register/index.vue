<router>
  {
    name:'register',
    path: '/register/'
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
