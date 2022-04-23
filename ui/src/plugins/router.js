import { createRouter, createWebHistory} from 'vue-router'
import HomePage from '@/views/HomePage.vue'
import ResultPage from "@/views/ResultPage";
import DetailPage from "@/views/DetailPage";

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
    },
    {
        path: '/detail/:gid',
        name: 'detail',
        component: DetailPage
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})
export default router