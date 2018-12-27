import Vue from 'vue';
import axios from 'axios';
import BootstrapVue from 'bootstrap-vue';
import Toaster from 'v-toaster';
import App from './components/Layout.vue';
import router from './router';
import store from './stores';
import WatchdogDateTime from '@/components/WatchdogDateTime';

Vue.config.productionTip = false;

Vue.prototype.$http = axios;

const token = localStorage.getItem('token');
if (token) {
  Vue.prototype.$http.defaults.headers.common['x-auth-token'] = token
}

Vue.use(BootstrapVue);
Vue.use(Toaster);
Vue.component(WatchdogDateTime.name, WatchdogDateTime);

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');
