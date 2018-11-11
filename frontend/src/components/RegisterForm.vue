<template>
  <b-form @submit="onSubmit"
          class="loginForm">
    <b-form-group id="loginInputGroup"
                  label="Username:"
                  label-for="loginInput">
      <b-form-input id="loginInput"
                    v-model="form.username"
                    required
                    placeholder="Enter username">
      </b-form-input>
    </b-form-group>
    <b-form-group id="passwordInputGroup"
                  label="Password:"
                  label-for="passwordInput">
      <b-form-input id="passwordInput"
                    type="password"
                    v-model="form.password"
                    required
                    placeholder="****">
      </b-form-input>
    </b-form-group>
    <b-form-group id="exampleGroup4">
      <b-form-checkbox value="me" v-model="form.checked">
        Remember me
      </b-form-checkbox>
    </b-form-group>
    <b-button type="submit" variant="primary">Login</b-button>
  </b-form>
</template>
<script>
export default {
  name: 'LoginForm',
  data() {
    return {
      form: {
        username: '',
        password: '',
        checked: [],
      },
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      alert(JSON.stringify(this.form));
    },
  },
};
</script>
