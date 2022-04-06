import { createRouter, createWebHistory} from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import ResultPage from "@/views/ResultPage";

const routes = [
    {
        path: '/',
        name: 'home',
        component: HomePage
    },
    {
        path: '/search',
        name: 'result',
        component: ResultPage
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})
export default router