<script>
export default {
  provide() {
    return {
      clear: this.clear
    };
  },
  data() {
    return {
      results: null,
      input: "",
      timer: null,
      loading: false
    };
  },

  methods: {
    clear() {
      this.results = null;
      this.timer = null;
      this.input = "";
    },
    searchEvent() {
      if (this.timer) {
        clearTimeout(this.timer);
      }
      if (this.loading) return;
      const val = this.input;
      if (!val || val.length < 2) {
        this.results = null;
        return;
      }
      // Items have already been requested

      this.timer = setTimeout(() => {
        this.quickSearch(val);
      }, 1000);
    },
    quickSearch(val) {
      this.loading = true;
      const query = encodeURIComponent(val);
      this.$store.dispatch("products/quickSearch", query).then(data => {
        this.results = data;
        this.loading = false;
      });
    }
  },

  render() {
    return this.$scopedSlots.default({
      input: this.input,
      results: this.results,
      searchEvent: this.searchEvent,
      loading: this.loading,
      clear: this.clear,
      inputProps: {
        value: this.input
      },
      inputEvents: {
        input: e => {
          this.input = e.trim();
        },
        keyup: this.searchEvent
      }
    });
  }
};
</script>

<style></style>
