<template>
  <div>
    <div class="loading" v-if="loading">
      Loading...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <b-tabs v-if="item">
      <b-tab title="Detail" active>
        <p>Title: {{item.title}}</p>
        <p>Description: {{item.description}}</p>
        <p>Created at:
          <WatchdogDateTime :time="item.createdAt"/>
        </p>
        <p>Modified at:
          <WatchdogDateTime :time="item.modifiedAt"/>
        </p>
      </b-tab>
      <b-tab title="Roles" active>
        <b-button :to="{ name: 'role:create', params: { serviceId: item._id }}">
          New service
        </b-button>
        <RoleListItem :item="item" v-for="item in roles" :key="item._id"/>
      </b-tab>
      <DebugTab :item="item"/>
    </b-tabs>
  </div>
</template>
<script>
  import WatchdogDateTime from "../WatchdogDateTime";
  import UserLink from "../UserLink";
  import RoleLink from "../RoleLink";
  import DebugTab from "../DebugTab";

  export default {
    name: 'ServiceDetail',
    components: {
      DebugTab,
      WatchdogDateTime,
      UserLink,
      RoleLink
    },
    data() {
      return {
        loading: false,
        item: {},
        roles: [],
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
        this.error = null;
        this.loading = true;
        // replace `getPost` with your data fetching util / API wrapper
        try {
          const resp = await this.$http.get(`/v1/service/${this.$route.params.id}`);
          const resp_roles = await this.$http.get(`/v1/service/${this.$route.params.id}/role`);
          this.loading = false;
          this.item = resp.data
          this.roles = resp_roles.data
        } catch (err) {
          this.error = err.toString();
          this.loading = false;
        }
      }
    }
  };
</script>
