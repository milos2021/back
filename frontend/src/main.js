import Vue from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import excel from 'vue-excel-export'
import { Service } from './service';
Vue.use(excel)



let vue = new Vue({
    // added by router plugin
    router,

    vuetify,
    render: h => h(App)
}).$mount('#app')

Service.prototype.$vue = vue;