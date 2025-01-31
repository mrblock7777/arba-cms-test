import { defineStore } from "pinia";
import axios from "axios";
import cookies from "vue-cookies";
import { useJwt } from "@vueuse/integrations/useJwt";

import { useRouter } from "vue-router";

const router = useRouter();

export const useAuthStore = defineStore("login", {
  state: () => ({
    user: null,
    token: null,
    error: null,
    isLogggedIn: false,
    currentUser: {},
  }),
  actions: {
    async checkCurrentUser() {
      const token = cookies.get("token");
      if (token) {
        console.log(token);
        const { payload } = useJwt(token);
        const user_id = payload.value.user_id;
        const response = await axios
          .get("/api/auth/user/" + user_id + "/")
          .catch((e) => console.log(e));
        this.currentUser = response.data;
        console.log(this.currentUser);
        this.token = token;
        this.isLogggedIn = true;
      }
    },
    async createUser(userData) {
      this.error = null;
      try {
          const response = await axios.post('/api/auth/register/', userData);
          this.user = response.data;
          console.log(this.user);
      } catch (error) {
          this.error = error.response ? error.response.data : error.message;
      } finally {
          this.loading = false;
      }
  },
    async login(username, password) {
      try {
        const response = await axios.post("/api/auth/login/", {
          username,
          password,
        });
        this.user = response.data.user;
        this.token = response.data.token;
        this.error = null;
        cookies.set("token", response.data.accessToken);
        console.log(response);

        this.checkCurrentUser();

      } catch (error) {
        this.error = error;
        console.log(error)
      }
    },
    logout() {
      this.user = null;
      this.token = null;
      this.error = null;
      cookies.remove("token");
    },
  },
});
