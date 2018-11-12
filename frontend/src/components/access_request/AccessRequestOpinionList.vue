<template>
  <table class="table">
    <thead>
    <th>OpinionId</th>
    <th>CreatedAt</th>
    <th>ModifiedAt</th>
    <th>UserId</th>
    <th>Status</th>
    </thead>
    <tbody>
    <tr v-for="item in items">
      <td>{{item._id}}</td>
      <td>{{item.createdAt}}</td>
      <td>{{item.modifiedAt}}</td>
      <td>{{item.userId}}</td>
      <td>{{item.status}}</td>
    </tr>
    </tbody>
  </table>
</template>
<script>
  export default {
    name: 'AccessRequestOpinionList',
    props: {
      items: {}
    }
  }
</script>
