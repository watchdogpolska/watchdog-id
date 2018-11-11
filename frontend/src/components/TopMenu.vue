<template>
  <div>
    <b-navbar toggleable="md" type="dark" variant="info">

      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

      <b-navbar-brand to="/">Watchdog ID</b-navbar-brand>
      <b-collapse is-nav id="nav_collapse">

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown>
            <template slot="button-content">Sitemap</template>
            <b-dropdown-item to='/login'>Login</b-dropdown-item>
            <b-dropdown-item to='/register'>Register</b-dropdown-item>
            <b-dropdown-item to='/about'>About</b-dropdown-item>
          </b-nav-item-dropdown>

          <!-- Using button-content slot -->
          <b-nav-item v-b-modal.loginModal v-if="!isLoggedIn">Login
          </b-nav-item>
          <b-nav-item v-b-modal.registerModal v-if="!isLoggedIn">Register
          </b-nav-item>
          <b-nav-item to="/access_request" v-if="isLoggedIn">Access request</b-nav-item>
          <b-nav-item href="#" v-if="isLoggedIn">Services</b-nav-item>
          <b-nav-item href="#" v-if="isLoggedIn">Users</b-nav-item>

          <b-nav-item-dropdown right v-if="isLoggedIn">
            <!-- Using button-content slot -->
            <template slot="button-content">
              <em>User</em>
            </template>
            <b-dropdown-item href="#">Profile</b-dropdown-item>
            <b-dropdown-item v-on:click="logout">Signout</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>

      </b-collapse>
    </b-navbar>

    <!-- the modal -->
    <b-modal id="loginModal">
      <template slot="modal-title">Login</template>
      <template slot="modal-ok">Login</template>
      <LoginForm/>
    </b-modal>
    <b-modal id="registerModal">
      <template slot="modal-title">Registration</template>
      <template slot="modal-ok">Register</template>
      <RegisterForm/>
    </b-modal>
  </div>
</template>
<script>
  import LoginForm from '@/components/LoginForm.vue';
  import RegisterForm from '@/components/RegisterForm.vue';

  export default {
    name: 'TopMenu',
    computed: {
      isLoggedIn: function () {
        return this.$store.getters.isLoggedIn
      }
    },
    methods: {
      logout: function () {
        this.$store.dispatch('logout')
          .then(() => {
            this.$toaster.success('Successfully logged out');
            this.$router.push('/')
          })
          .catch(err => {
            this.$toaster.error('An error occured! ' + err.response.data.error);
            console.log(err)
          });
      }
    },
    components: {LoginForm, RegisterForm},
  };
</script>
