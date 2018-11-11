<template>
  <b-tab title="Debug">
    <pre>{{item}}</pre>
  </b-tab>
</template>
<script>
  export default {
    name: 'DebugTab',
    props: {
      item: {}
    }
  }
</script>
