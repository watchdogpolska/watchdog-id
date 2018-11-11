<script>
  import TopMenu from './TopMenu.vue';
import 'v-toaster/dist/v-toaster.css'
  export default {
    components: {TopMenu},
  };
</script>
<template>
  <div>
    <TopMenu/>
    <div class="container">
      <router-view></router-view>
    </div>
  </div>
</template>

<style>
  body {
    /*background-color: #f1f1f1;*/
  }

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }

  #nav {
    padding: 30px;
  }

  #nav a {
    font-weight: bold;
    color: #2c3e50;
  }

  #nav a.router-link-exact-active {
    color: #42b983;
  }
</style>
