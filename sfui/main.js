import App from './App'

import { aes_encrypt, aes_decrypt } from '@/encode/util.js';
Vue.prototype.aes_encrypt = aes_encrypt;
Vue.prototype.aes_decrypt = aes_decrypt;

// #ifndef VUE3
import Vue from 'vue'
import './uni.promisify.adaptor'
Vue.config.productionTip = false
App.mpType = 'app'
const app = new Vue({
  ...App
})
app.$mount()
// #endif




// #ifdef VUE3
import { createSSRApp } from 'vue'
export function createApp() {
  const app = createSSRApp(App)
  return {
    app
  }
}
// #endif