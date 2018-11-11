import Vue from 'vue';
import Router from 'vue-router';
import Home from '@/views/Home.vue';
import About from '@/views/About.vue';
import AccessRequestPage from '@/views/AccessRequestPage.vue';

Vue.use(Router);

const protectedRoutes = [
  {
      path: '',
      component: Home,
    },
    {
      path: '/about',
      component: About,
    },
  {
    path: '/access_request',
    component: AccessRequestPage,
    children: [
      {
        path: '/access_request/',
        component: () => import('@/components/AccessRequestList.vue'),
        name: 'access_request:list',
      },
      {
        path: '/access_request/:id/',
        component: () => import('@/components/AccessRequestDetail.vue'),
        name: 'access_request:detail',
      },
    ]
  }
];

protectedRoutes.forEach(x => x.meta = {...x.meta, requiresAuth: true});

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/login',
      component: () => import(/* webpackChunkName: "login" */ '@/views/auth/Login.vue'),
    },
    {
      path: '/register',
      component: () => import(/* webpackChunkName: "register" */ '@/views/auth/Register.vue'),
    },
    ...protectedRoutes
  ],
});
// router.beforeEach((to, from, next) => {
//   if (to.matched.some(record => record.meta.requiresAuth)) {
//     // if (store.getters.isLoggedIn) {
//     //   next()
//     //   return
//     // }
//     next('/login')
//   } else {
//     next()
//   }
// });

export default router;
