<template>
    <v-container class="d-flex justify-center align-center fill-height" fluid>
        <v-card width="400">
            <v-card-title>
                <span class="headline">Sign Up</span>
            </v-card-title>
            <v-card-text>
                <v-form ref="form" v-model="valid">
                    <v-text-field v-model="firstName" :rules="[rules.required]" label="First Name"
                        required></v-text-field>
                    <v-text-field v-model="lastName" :rules="[rules.required]" label="Last Name"
                        required></v-text-field>
                    <v-text-field v-model="username" :rules="[rules.required]" label="Username" required></v-text-field>
                    <v-text-field v-model="email" :rules="[rules.required, rules.email]" label="Email"
                        required></v-text-field>
                    <v-text-field v-model="password" :rules="[rules.required, rules.min(6)]" label="Password"
                        type="password" required></v-text-field>
                    <v-text-field v-model="confirmPassword" :rules="[rules.required, rules.matchPassword]"
                        label="Confirm Password" type="password" required></v-text-field>
                    <router-link to="/auth/login">Already have an account? Sign in now</router-link>
                    <br />
                    <v-btn class="my-4" color="primary" @click="submit()">Sign Up</v-btn>
                </v-form>
            </v-card-text>
        </v-card>
    </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth'

const valid = ref(false);
const firstName = ref('');
const lastName = ref('');
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const form = ref(null);
const router = useRouter();
const authStore = useAuthStore();

const rules = {
    required: value => !!value || 'Required.',
    email: value => /.+@.+\..+/.test(value) || 'E-mail must be valid.',
    min: length => value => value.length >= length || `Min ${length} characters`,
    matchPassword: value => value === password.value || 'Passwords must match'
};

const submit = async () => {
    const validate = await form.value.validate();
    if (validate.valid) {
        // Handle sign up logic here
        try {
            await authStore.createUser({
                first_name: firstName.value,
                last_name: lastName.value,
                username: username.value,
                email: email.value,
                password: password.value
            });
            router.push('/auth/login');
        } catch (error) {
            console.log(error);
        }

    }
};

</script>

<style scoped>
.headline {
    font-weight: bold;
}
</style>