import { defineStore } from 'pinia';
import axios from 'axios';
import { useAuthStore } from '../auth'

const authStore = useAuthStore();

export const useProfileStore = defineStore('profile', {
    state: () => ({
        user: null,
        loading: false,
        error: null,
    }),
    actions: {
        async updateUser(userData) {
            // console.log(userData)
            this.loading = true;
            this.error = null;
            try {
                const response = await axios.put(`/auth/user/${userData.id}/`, userData,{
                    headers: {
                        Authorization: `Bearer ${authStore.token}`,
                    },
                });
                this.user = response.data;
                console.log(this.user)
            } catch (error) {
                this.error = error.response ? error.response.data : error.message;
            } finally {
                this.loading = false;
            }
        },
        async getUser(userId) {
            this.error = null;
            try {
                const response = await axios.get(`/auth/user/${userId}/`);
                this.user = response.data;
                console.log(this.user)
            } catch (error) {
                this.error = error.response ? error.response.data : error.message;
            } finally {
                this.loading = false;
            }
        },
    },
});