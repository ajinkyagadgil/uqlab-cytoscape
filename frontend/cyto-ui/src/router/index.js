import Vue from 'vue'
import Router from 'vue-router'
import EditGraph from '../components/EditGraph.vue'
import GraphListing from '../components/GraphListing.vue'

Vue.use(Router)
export default new Router({
    routes: [
        { path: '/', component: GraphListing },
        { path: '/graph/:id', name:"Graph", component: EditGraph },
    ]
})

