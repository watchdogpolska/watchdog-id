<template>
  <router-link
    :to="{ name: 'user:detail', params: { id: id }}"
  >
    {{name}}
  </router-link>
</template>
<script>
  export default {
    name: 'UserLink',
    data() {
      return {
        name: ''
      }
    },
    props: {
      id: ''
    },
    created() {
      this.fetchData()
    },
    methods: {
      async fetchData() {
        try {
          const resp = await this.$http.get(`/v1/user/${this.id}`);
          this.name = resp.data.username
        } catch (err) {
          this.name = this.id
        }
      }
    }
  }
</script>
