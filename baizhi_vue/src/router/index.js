import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)
import Login from "../components/Login";
import Register from "../components/Register";
import Course from "../components/Course";
import CourseDetail from "../components/CourseDetail";
import Cart from "../components/Cart";
import Order from "../components/Order";
import OrderSuccess from "../components/OrderSuccess";
import OrderList from "../components/OrderList";
import Index from "../components/Index";

export default new Router({

  mode : "history",
  routes: [
    {
      path: '/',
      name: "index",
      component: Index
    },
    {
      path: '/index',
      name: "index",
      component: Index
    },
    {
      path: '/login',
      name: "Login",
      component: Login
    },
    {
      path: '/user/register',
      name: "Register",
      component: Register
    },
    {
      path: '/course',
      name: "Course",
      component: Course
    },
    {
      path: '/course/detail/:id',
      name: "CourseDetail",
      component: CourseDetail
    },
    {
      path: '/cart',
      name: "Cart",
      component: Cart
    },
    {
      path: '/order',
      name: "Order",
      component: Order
    },
    {
      path: '/payments/result',
      name: "OrderSuccess",
      component: OrderSuccess
    },
    {
      path: '/orderlist',
      name: 'OrderList',
      component: OrderList
    }


  ]
})
