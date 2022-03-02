import Vue from 'vue'
import App from './App.vue'
import VueCytoscape from 'vue-cytoscape'
import vuetify from './plugins/vuetify'
import router from './router'
Vue.config.productionTip = false
Vue.use(VueCytoscape)
new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
