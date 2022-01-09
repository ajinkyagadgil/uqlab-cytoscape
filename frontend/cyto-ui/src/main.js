import Vue from 'vue'
import App from './App.vue'
import VueCytoscape from 'vue-cytoscape'
Vue.config.productionTip = false
Vue.use(VueCytoscape)
new Vue({
  render: h => h(App),
}).$mount('#app')
