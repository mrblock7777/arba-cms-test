/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueCookies from 'vue-cookies'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

axios.defaults.baseURL = import.meta.env.VITE_API_URL

const app = createApp(App)
app.use(VueAxios, axios)
app.use(VueCookies, {expires:'1d'})

registerPlugins(app)


app.mount('#app')
