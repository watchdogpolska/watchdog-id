<template>
  <div class="col-6 offset-3 box">
    <h2>Log in</h2>
    <p>You dont have an account yet?
      <router-link to="/register">Register</router-link>
      !
    </p>
    <LoginForm/>
  </div>
</template>
<script>
import LoginForm from '../../components/LoginForm.vue';

export default {
  components: {
    LoginForm,
  },

};
</script>
