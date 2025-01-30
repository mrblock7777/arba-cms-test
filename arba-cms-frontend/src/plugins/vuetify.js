/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides

const customTheme = {
  dark: false,
  colors:{
    primary: '#BC2525'
  }
}
export default createVuetify({
  theme: {
    defaultTheme: 'customTheme',
    themes: {
      customTheme
    }
  },
})
