<template>
  <v-app>
    <v-app-bar height="50" app color="primary" dark>
      <v-toolbar-title>
        <router-link class="text-decoration-none text-white" to="/">Arba</router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="!authStore.isLogggedIn" color="white" @click="$router.push('/auth/login')">Login</v-btn>
      <div v-else>
        <span class="mr-4">Hello, @{{ authStore.currentUser.username }}</span>
        <v-btn color="white" @click="logout()">Logout</v-btn>
      </div>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router';

const router = useRouter();
const authStore = useAuthStore();

const logout = () => {
  authStore.logout();
  router.go();
}

</script>

<style scoped></style>