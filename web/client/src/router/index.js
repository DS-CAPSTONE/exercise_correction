import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "Home",
            component: () => import("../views/Home.vue"),
        },
        {
            path: "/live",
            name: "LiveStreaming",
            component: () => import("../views/LiveStreaming.vue"),
        },
        {
            path: "/video",
            name: "VideoStreaming",
            component: () => import("../views/VideoStreaming.vue"),
        },
        {
            path: "/realtime",
            name: "RealTimeWebsite",
            beforeEnter() {
                // Redirect to the external URL
                window.location.href = "http://localhost:8501/";
            },
        },
        {
            path: "/:pathMatch(.*)*",
            redirect: { name: "Home" },
        },
    ],
});

export default router;
