import { Service } from '../service';
class OrientationService extends Service {
    chartMode = false;
    initialLoad = true;

    constructor() {
        super();
    }

    getChartMode() {
        return this.chartMode;
    }

    setChartMode(val) {
        this.chartMode = val;
    }

    getInitialLoad() {
        return this.initialLoad;
    }

    setInitialLoad(val) {
        this.initialLoad = val;
    }

}
export default new OrientationService();