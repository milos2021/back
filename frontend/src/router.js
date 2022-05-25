import VueRouter from 'vue-router'
import Tiket from './views/Tiket';
import CashFlow from './views/CashFlow';
import RepStats from './views/RepStats';
import SlipDetailedPreview from './views/SlipDetailedPreview';
import Sport from './views/Sport';
import AdvancedStatisticForPeriod from './views/AdvancedStatisticForPeriod'
import Vue from 'vue';


Vue.use(VueRouter);

const routes = {
    mode: 'history',
    routes: [{
            path: '/reporting',
            component: Tiket
        },
        {
            path: '/reporting/Tiket',
            component: Tiket
        },
        {
            path: '/reporting/Sport',
            component: Sport
        },
        {
            path: '/reporting/RepStats',
            component: RepStats
        },
        {
            path: '/reporting/Cashflow',
            component: CashFlow
        },
        {
            path: '/reporting/SlipDetailedPreview',
            component: SlipDetailedPreview
        },
        {
            path: '/reporting/AdvancedStatisticForPeriod',
            component: AdvancedStatisticForPeriod
        }
    ]

};

const router = new VueRouter(routes);

export default router