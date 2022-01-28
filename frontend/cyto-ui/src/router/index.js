import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '../components/HelloWorld.vue'
import GraphListing from '../components/GraphListing.vue'

Vue.use(Router)

export default new Router({
    routes: [
        { path: '/', component: GraphListing },
        { path: '/graph', component: HelloWorld },
    ]
})
