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
        component: () => import('@/components/access_request/AccessRequestList.vue'),
        name: 'access_request:list',
      },
      {
        path: '/access_request/:id',
        component: () => import('@/components/access_request/AccessRequestDetail.vue'),
        name: 'access_request:detail',
      },
    ]
  },
  {
    path: '/service',
    component: () => import('@/views/ServicePage.vue'),
    children: [
      {
        path: '/service/',
        component: () => import('@/components/service/ServiceList.vue'),
        name: 'service:list',
      },
      {
        path: '/service/new',
        component: () => import('@/components/service/ServiceForm.vue'),
        name: 'service:create',
      },
      {
        path: '/service/:id',
        component: () => import('@/components/service/ServiceDetail.vue'),
        name: 'service:detail',
      },
      {
        path: '/service/:id/update',
        component: () => import('@/components/service/ServiceForm.vue'),
        name: 'service:update',
      },
    ]
  },
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