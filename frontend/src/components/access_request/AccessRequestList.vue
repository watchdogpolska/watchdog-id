<template>
  <div>
    <div class="loading" v-if="loading">
      Loading...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>
    <AccessRequestListItem :item="item" v-for="item in items"/>
  </div>
</template>
<script>
  import AccessRequestListItem from "./AccessRequestListItem";

  export default {
    name: 'AccessRequestList',
    components: {AccessRequestListItem},
    data() {
      return {
        loading: false,
        items: null,
        error: null
      }
    },
    created() {
      // fetch the data when the view is created and the data is
      // already being observed
      this.fetchData()
    },
    watch: {
      // call again the method if the route changes
      '$route': 'fetchData'
    },
    methods: {
      async fetchData() {
        this.error = this.post = null;
        this.loading = true;
        // replace `getPost` with your data fetching util / API wrapper
        try {
          const resp = await this.$http.get('/v1/access_request');
          this.loading = false;
          this.items = resp.data
        } catch (err) {
          this.error = err.toString();
          this.loading = false;
        }
      }
    }
  }
</script>
