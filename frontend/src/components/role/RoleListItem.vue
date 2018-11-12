<template>
  <div class="list-item">
    <h2>
      <router-link
        :to="{ name: 'service:detail', params: { id: item._id, service: item.serviceId }}"
      >
        {{item.createdAt}}
      </router-link>
    </h2>
    <b-button to="#" variant="primary">Go somewhere</b-button>
  </div>
</template>
<script>
  export default {
    name: 'RoleListItem',
    props: {
      item: {}
    }
  }
</script>
