<template>
    <v-container class="d-flex justify-center align-center fill-height" fluid>
        <v-card width="400" class="pa-4">
            <v-card-title>
                <span class="headline">Login</span>
            </v-card-title>
            <v-card-text>
                <!-- <v-form ref="form" v-model="valid" lazy-validation> -->
                <v-text-field v-model="username" label="Username" type="text" required></v-text-field>
                <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
                <router-link to="/auth/signup">Don't have an account? Sign up</router-link>
                <br />
                <v-btn class="my-4" @click="login()" color="primary">Login</v-btn>
                <!-- </v-form> -->
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router';

const router = useRouter();
const username = ref('');
const password = ref('');
const authStore = useAuthStore();

const login = async () => {
    console.log('Username:', username.value);
    console.log('Password:', password.value);

    await authStore.login(username.value, password.value);
    if (!authStore.error) {
        router.push("/");
    }
    console.log(authStore.error)

};
</script>

<style scoped>
.fill-height {
    height: 100vh;
}
</style>