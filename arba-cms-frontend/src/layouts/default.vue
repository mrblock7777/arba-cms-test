<template>
  <v-app>
    <v-app-bar height="50" app color="primary" dark>
      <v-app-bar-nav-icon v-show="!lgAndUp && authStore.isLogggedIn" variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>
        <router-link class="text-decoration-none text-white" to="/">
          <span v-if="lgAndUp">Arba</span>
          <v-icon v-else>mdi-home</v-icon>
        </router-link>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="!authStore.isLogggedIn" color="white" @click="$router.push('/auth/login')">Login</v-btn>
      <div v-else>
        <span class="mr-4">Hello, @{{ authStore.currentUser.username }}</span>
        <v-btn color="white" @click="logout()">Logout</v-btn>
      </div>
    </v-app-bar>
    <v-navigation-drawer width="300"  v-model="drawer" temporary>
      <v-card width="250" class="ma-4">
        <v-img src="https://salondesmaires-ain.fr/wp-content/uploads/2014/10/speaker-3.jpg" height="150px"></v-img>
        <v-card-subtitle class="mt-4">{{ authStore.currentUser.first_name }} {{ authStore.currentUser.last_name
          }}</v-card-subtitle>
        <v-card-text>
          <v-list>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>Email: {{ authStore.currentUser.email }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
          <v-tooltip text="Add a new post">
            <template v-slot:activator="{ props }">
              <v-btn v-bind="props" color="primary" icon="mdi-plus" @click="$router.push('/post/create')"></v-btn>
            </template>
          </v-tooltip>
          <v-tooltip text="Edit Profile and View Your Posts">
            <template v-slot:activator="{ props }">
              <v-btn v-bind="props" class="mx-2" color="indigo" icon="mdi-panorama"
                @click="$router.push('/profile/' + authStore.currentUser.id)"></v-btn>
            </template>
          </v-tooltip>
        </v-card-text>
      </v-card>
    </v-navigation-drawer>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue';
import { useDisplay } from 'vuetify'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router';

const drawer = ref(false)
const router = useRouter();
const { lgAndUp } = useDisplay()
const authStore = useAuthStore();


const logout = () => {
  authStore.logout();
  router.go();
}

</script>

<style scoped></style>