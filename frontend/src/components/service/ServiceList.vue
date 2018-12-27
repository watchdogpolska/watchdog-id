<template>
  <div>
    <div class="loading" v-if="loading">
      Loading...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <b-button :to="{ name: 'service:create'}">
      New service
    </b-button>
    <b-btn v-b-modal.modal1>New service</b-btn>
    <ServiceListItem :item="item" v-for="item in items" :key="item._id"/>
    <ServiceForm/>
  </div>
</template>
<script>
  import ServiceListItem from "./ServiceListItem";
  import ServiceForm from "./ServiceForm";

  export default {
    name: 'ServiceList',
    components: {ServiceListItem, ServiceForm},
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
          const resp = await this.$http.get('/v1/service');
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
