// main.ts
import Vue from 'vue';
import App from './App.vue';
import VueRouter, { Route } from 'vue-router';
import keycloak from '@/path-to-keycloak.ts';

Vue.config.productionTip = false;

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    component: Home,
    meta: { requiresAuth: true },
  },
  // Other routes...
];

const router = new VueRouter({
  routes,
});

router.beforeEach((to: Route, from: Route, next: any) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!keycloak.authenticated) {
      keycloak.login();
    } else {
      next();
    }
  } else {
    next();
  }
});

new Vue({
  render: (h) => h(App),
  router,
}).$mount('#app');
