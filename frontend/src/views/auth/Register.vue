<template>
  <div class="col-6 offset-3 box">
    <h2>Registration</h2>
    <p>You already have an account, <router-link to="/login">log in</router-link>!</p>
    <RegisterForm/>

  </div>
</template>


<script>
import RegisterForm from '@/components/RegisterForm.vue';

export default {
  components: {
    RegisterForm,
  },
};
</script>
