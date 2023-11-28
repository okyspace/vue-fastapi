// YourVueComponent.vue
<template>
  <div>
    <p v-if="authenticated">Authenticated as {{ userInfo.username }}</p>
    <button @click="login" v-if="!authenticated">Login</button>
    <button @click="logout" v-if="authenticated">Logout</button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import Component from 'vue-class-component';
import keycloak from '@/path-to-keycloak.ts';

@Component
export default class YourVueComponent extends Vue {
  authenticated: boolean = false;
  userInfo: any = {};

  mounted() {
    keycloak.init({ onLoad: 'login-required' }).then((authenticated) => {
      this.authenticated = authenticated;
      if (authenticated) {
        keycloak.loadUserInfo().then((userInfo) => {
          this.userInfo = userInfo;
        });
      }
    });
  }

  login() {
    keycloak.login();
  }

  logout() {
    keycloak.logout();
  }
}
</script>
