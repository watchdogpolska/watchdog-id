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
        <p>Comment: {{item.comment}}</p>
        <p>Created at: <WatchdogDateTime :time="item.createdAt"/></p>
        <p>Modified at: <WatchdogDateTime :time="item.modifiedAt"/></p>
      </b-tab>
      <b-tab title="Users">
        <table class="table">
          <thead>
            <th>UserID</th>
          </thead>
          <tbody>
          <tr v-for="user_id in item.usersId">
            <td><UserLink :id="user_id"/></td>
          </tr>
          </tbody>
        </table>
      </b-tab>
      <b-tab title="Roles">
        <table class="table">
          <thead>
            <th>Role</th>
          </thead>
          <tbody>
          <tr v-for="role_id in item.rolesId">
            <td><RoleLink :id="role_id"/></td>
          </tr>
          </tbody>
        </table>
      </b-tab>
      <b-tab title="Opinions">
        <AccessRequestOpinionList :items="item.opinions"/>
      </b-tab>
      <b-tab title="Events">
        <AccessRequestEventList :items="item.events"/>
      </b-tab>
      <DebugTab :item="item"/>
    </b-tabs>
  </div>
</template>
<script>
  import WatchdogDateTime from "../WatchdogDateTime";
  import AccessRequestOpinionList from "./AccessRequestOpinionList";
  import AccessRequestEventList from "./AccessRequestEventList";
  import UserLink from "../UserLink";
  import RoleLink from "../RoleLink";
  import DebugTab from "../DebugTab";

  export default {
    name: 'AccessRequestDetail',
    components: {
      DebugTab,
      AccessRequestEventList,
      AccessRequestOpinionList,
      WatchdogDateTime,
      UserLink,
      RoleLink
    },
    data() {
      return {
        loading: false,
        item: {},
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
          const resp = await this.$http.get(`/v1/access_request/${this.$route.params.id}`);
          this.loading = false;
          this.item = resp.data
        } catch (err) {
          this.error = err.toString();
          this.loading = false;
        }
      }
    }
  };
</script>
