// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

//导入全局样式
import '../static/css/global.css'
import "../static/js/gt"

import VideoPlayer from 'vue-video-player'
require('video.js/dist/video-js.css')
require('vue-video-player/src/custom-theme.css')
Vue.use(VideoPlayer)


Vue.prototype.$axios=axios;
Vue .use(Element)


Vue.config.productionTip = false


//自定义配置
// import settings from './settings';
// Vue.prototype.$settings=settings;

//状态机
import store from './store/index';


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
