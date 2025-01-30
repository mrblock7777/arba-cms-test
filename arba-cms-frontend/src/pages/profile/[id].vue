<template>
    <v-container>
        <v-form>
            <v-card class="my-4 pa-4">
                <v-card-title>Profile</v-card-title>
                <v-img src="https://salondesmaires-ain.fr/wp-content/uploads/2014/10/speaker-3.jpg"
                    height="150px"></v-img>
                <v-card-text>
                    <v-flex>
                        <span class="text-h6">Username: {{ profile.username }}</span>
                    </v-flex>
                    <v-flex>
                        <v-text-field v-model="profile.first_name" label="First Name" :readonly="authStore.currentUser.id !== profile.id" required></v-text-field>
                    </v-flex>
                    <v-flex>
                        <v-text-field v-model="profile.last_name" label="Last Name" :readonly="authStore.currentUser.id !== profile.id" required></v-text-field>
                    </v-flex>
                    <v-flex>
                        <v-text-field v-model="profile.email" label="Email" :readonly="authStore.currentUser.id !== profile.id" required></v-text-field>
                    </v-flex>
                    <v-btn v-if="authStore.currentUser.id === profile.id" class="float-right" color="primary" @click="saveProfile">Save</v-btn>
                </v-card-text>
            </v-card>
        </v-form>
        <span class="text-h4">{{ authStore.currentUser.id === profile.id ? 'Your' : profile.username + "\'s" }} Posts</span>
        <ListPost/>
    </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth'
import { useProfileStore } from '@/stores/profile'
import { onMounted, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import ListPost from '../post/List'

const route = useRoute();
const authStore = useAuthStore();
const profileStore = useProfileStore();
const profile = ref({
    username: '',
    first_name: '',
    last_name: '',
    email: '',
});

const saveProfile = async () => {
    // Save profile logic here
    profile.value = {
        ...profile.value,
        id: authStore.currentUser.id,
    }
    console.log('Profile:', profile.value);
    await profileStore.updateUser(profile.value);
}
const getProfile = async () => {
    // Get profile logic here
    await profileStore.getUser(route.params.id);
    profile.value = profileStore.user
}

onMounted(() => {
    
})
onBeforeMount(() => {
    getProfile();
});

</script>

<style scoped>
.v-container {
    max-width: 600px;
    margin: 0 auto;
}
</style>