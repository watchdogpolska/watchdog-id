<template>
  <b-modal id="modal1" title="Bootstrap-Vue" @ok="onSubmit">

    <b-form @submit="onSubmit"
            class="loginForm">
      <b-form-group id="titleInputGroup"
                    label="Title:"
                    label-for="serviceInput">
        <b-form-input id="titleInput"
                      v-model="form.title"
                      required
                      placeholder="Enter title">
        </b-form-input>
      </b-form-group>
      <b-form-group id="description"
                    label="Description:"
                    label-for="descriptionGroup">
        <b-form-textarea id="descriptionGroup"
                         v-model="form.description">
        </b-form-textarea>
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
      <!--<b-button type="submit" variant="primary">Create</b-button>-->
    </b-form>
  </b-modal>
</template>
<script>
  import WatchdogDateTime from "../WatchdogDateTime";
  import UserLink from "../UserLink";
  import RoleLink from "../RoleLink";
  import DebugTab from "../DebugTab";

  export default {
    name: 'ServiceForm',
    components: {
      DebugTab,
      WatchdogDateTime,
      UserLink,
      RoleLink
    },
    data() {
      return {
        form: {},
        loading: false,
        item: {},
        error: null
      }
    },
    methods: {
      onSubmit: function (evt) {
        evt.preventDefault();
        this.$store.dispatch('service/addItem', this.form)
          .then(resp => {
            this.$toaster.success('Successfully added new service.');
            this.$router.push({
              name: 'service:detail',
              params: {id: resp.data._id}
            })
          })
          .catch(err => {
            this.$toaster.error('An error occured! ' + err.response.data.error);
            console.log(err)
          });
      },
    }
  };
</script>
