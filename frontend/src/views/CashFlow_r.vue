<template>
  <div>
    <v-container fluid>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            :items="methods"
            item-value="id"
            item-text="title"
            v-model="methodDefault"
            label="Payment Method"
            v-on:change="filterByMethod"
          ></v-select>
        </v-col>
      </v-row>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            :items="periods"
            item-value="id"
            item-text="title"
            v-model="periodDefault"
            label="Period"
            v-on:change="filterByPeriod"
          ></v-select>
        </v-col>
      </v-row>
      <v-row align="center" v-if="otherLists.showMonth">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            :items="months"
            item-value="id"
            item-text="title"
            v-model="monthDefault"
            label="Month"
            v-on:change="filterByMonth"
          ></v-select>
        </v-col>
      </v-row>
      <!-- godina -->
      <v-row align="center" v-if="otherLists.showYear">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            :items="years"
            item-value="id"
            item-text="title"
            v-model="yearDefault"
            label="Year"
            v-on:change="filterByYear"
          ></v-select>
        </v-col>
      </v-row>
      <!-- vikend -->
      <v-row id="weekend" v-if="otherLists.showCalendar">
   
    <v-col
      cols="12"
      sm="6"
    >
      <v-menu
        ref="menu"
        v-model="menu"
        :close-on-content-click="false"
        :return-value.sync="dates"
        transition="scale-transition"
        offset-y
        min-width="auto"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-combobox
            v-model="dates"
            multiple
            chips
            small-chips
            label="Select dates"
            prepend-icon="mdi-calendar"
            readonly
            v-bind="attrs"
            v-on="on"
          ></v-combobox>
        </template>
        <v-date-picker
          v-model="dates"
          multiple
          dark
          no-title
          scrollable
        >
          <v-spacer></v-spacer>
          
          <v-btn
            text
            color="primary"
            @click="$refs.menu.save(dates)"
          >
            OK
          </v-btn>
          <v-btn
            text
            color="primary"
            @click="menu = false"
          >
            Close
          </v-btn>
          <v-btn
            text
            color="primary"
            @click="dates = []"
          >
            Clear
          </v-btn>
        </v-date-picker>
      </v-menu>
    </v-col>
  </v-row>
    </v-container>
    <v-container fluid>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-btn
            color="primary"
            elevation="2"
            outlined
            plain
            raised
            v-on:click="getData"
            >Search</v-btn
          >
          <export-excel
            class="btn btn-default"
            :data="json_data"
            type="csv"
            :name="todayDateFile"
            v-if="!initialLoad && tiketi.length>0"
          >
            <img
              src="@/assets/excel.png"
              style="margin-top:-8px; margin-left:3px; width:40px; cursor:pointer"
            />
          </export-excel>
        </v-col>
      </v-row>
    </v-container>
    <v-layout v-if="!initialLoad" v-resize="onResize" column style="padding-top:56px">
      <v-data-table
        id="report2"
        :headers="headers"
        :hide-default-header="!isMobile"
        :page.sync="page"
        :items-per-page="itemsPerPage"
        hide-default-footer
        :items="tickets"
        :class="{ cashflowMobile: isMobile }"
        item-key="name"
        :loading="loadTable"
        @page-count="pageCount = $event"
        no-data-text="No data"
        loading-text="Data is loading..."
      >
        <template v-if="!isMobile" v-slot:header="{ props }">
          <tr style="text-align:center">
            <th></th>
            <th
              colspan="3"
              style="border-left:1px solid black; border-right:1px solid black; border-bottom:1px solid black"
            >
              Deposit
            </th>
            <th colspan="3" style="border-right:1px solid black; border-bottom:1px solid black">Withdraw</th>
            <th colspan="3" style="border-right:1px solid black; border-bottom:1px solid black">Promo Achivement</th>
            <th colspan="2" style="border-right:1px solid black; border-bottom:1px solid black">Standard Balance</th>
          </tr>
          <tr style="text-align:center">
            <th class="mainHeader"></th>
            <th
              class="mainHeader"
              style="text-align:left; padding-left:15px; padding-top:10px"
              v-for="head in props.headers"
              :key="head.value"
            >
              {{ head.text.toUpperCase() }}
            </th>
          </tr>
          <tr>
            <th
              style="text-align:left; padding-left:15px; padding-bottom:5px; border-right:1px solid black; padding-top:5px; border-top:1px solid black; border-bottom:1px solid black"
            >
              Overall
            </th>
            <th
              style="text-align:left; padding-left:15px; border-right:1px solid black; padding-bottom:5px; padding-top:5px; border-top:1px solid black; border-bottom:1px solid black"
            >
              {{ overalls.deposit_users }}
            </th>
            <th
              style="text-align:left; padding-left:15px; border-right:1px solid black; padding-bottom:5px; padding-top:5px; border-top:1px solid black; border-bottom:1px solid black"
            >
              {{ overalls.deposit_number }}
            </th>
            <th
              style="text-align:left; padding-left:15px; border-right:1px solid black; padding-bottom:5px; padding-top:5px; border-top:1px solid black; border-bottom:1px solid black"
            >
              {{ overalls.deposit_sum }}
            </th>
            <th
              style="text-align:left; padding-left:15px; border-right:1px solid black; padding-bottom:5px; padding-top:5px; border-top:1px solid black; border-bottom:1px solid black"
            >
              {{ overalls.withdraw_users }}
            </th>
            <th
              style="text-align:left; padding-left:15px; border-right:1px solid black; padding-bottom:5px; padding-top:5px; border-top:1px solid black; border-bottom:1px solid black"
            >
                          {{ overalls.withdraw_number }}

            </th>
            <th
              style="text-align:left; padding-left:15px; border-right:1px solid black; padding-bottom:5px; padding-top:5px; border-top:1px solid black; border-bottom:1px solid black"
            >
              {{ overalls.withdraw_sum }}
            </th>
            <th
              style="text-align:left; padding-left:15px; border-right:1px solid black; padding-bottom:5px; padding-top:5px; border-top:1px solid black; border-bottom:1px solid black"
            >
              {{ overalls.promo_users }}
            </th>
            <th
              style="text-align:left; padding-left:15px; border-right:1px solid black; padding-bottom:5px; padding-top:5px; border-top:1px solid black; border-bottom:1px solid black"
            >
              {{ overalls.promo_number }}
            </th>
                        <th
              style="text-align:left; padding-left:15px; border-right:1px solid black;  padding-bottom:5px; padding-top:5px; border-top:1px solid black; border-bottom:1px solid black"
            >
              {{ overalls.promo_sum }}
            </th>
            <th
              style="text-align:left; padding-left:15px; border-right:1px solid black; padding-bottom:5px; padding-top:5px; border-top:1px solid black; border-bottom:1px solid black"
            >
              {{ overalls.std_balance_start }}
            </th>
            <th
              style="text-align:left; padding-left:15px; border-right:1px solid black; padding-bottom:5px; padding-top:5px; border-top:1px solid black; border-bottom:1px solid black"
            >
              {{ overalls.std_balance_end }}
            </th>
          </tr>
        </template> 
        <template v-slot:item="{ item }">
          <tr v-if="!isMobile">
            <td>{{ item.Opseg }}</td>
            <td class="text-xs-right">{{ item.deposit_users }}</td>
            <td class="text-xs-right">{{ item.deposit_number }}</td>
            <td class="text-xs-right">{{ item.deposit_sum }}</td>
            <td class="text-xs-right">{{ item.withdraw_users }}</td>
            <td class="text-xs-right">{{ item.withdraw_number }}</td>
            <td class="text-xs-right">{{ item.withdraw_sum }}</td>
            <td class="text-xs-right">{{ item.promo_users }}</td>
            <td class="text-xs-right">{{ item.promo_number }}</td>
            <td class="text-xs-right">{{ item.promo_sum }}</td>
            <td class="text-xs-right">{{ item.std_balance_start }}</td>
            <td class="text-xs-right">{{ item.std_balance_end }}</td>

          </tr>
          <tr id="mobileRow" v-else>
            <td
              style="border-top:thin solid rgba(0,0,0,0.12); border-bottom:none"
            >
              <ul class="flex-content">
                <li class="flex-item" data-label="YEAR">
                  {{ item.Opseg }}
                </li>
                <li class="flex-item" data-label="D-USERS">
                  {{ item.deposit_users }}
                </li>
                <li class="flex-item" data-label="D-NUMBER">
                  {{ item.deposit_number }}
                </li>
                <li class="flex-item" data-label="D-SUM">
                  {{ item.deposit_sum }}
                </li>
                <li class="flex-item" data-label="W-USERS">
                  {{ item.withdraw_users }}
                </li>
                <li class="flex-item" data-label="W-NUMBER">
                  {{ item.withdraw_number }}
                </li>
                <li class="flex-item" data-label="W-SUM">
                  {{ item.withdraw_sum }}
                </li>
                <li class="flex-item" data-label="P-USERS">
                  {{ item.promo_users }}
                </li>
                <li class="flex-item" data-label="P-NUMBER">
                  {{ item.promo_number }}
                </li>
                <li class="flex-item" data-label="P-SUM">
                  {{ item.promo_sum }}
                </li>
                <li class="flex-item" data-label="B-START">
                  {{ item.std_balance_start }}
                </li>
                <li class="flex-item" data-label="B-END">
                  {{ item.std_balance_end }}
                </li>
              </ul>
            </td>
          </tr>
        </template>
      </v-data-table>
      <!-- <template v-if="chartMode">
        <v-row style="margin-left:10px" align="center">
          <v-col class="d-flex" cols="12" lg="4" md="4" sm="6">
            <v-select
              :items="chartFilterData"
              item-value="id"
              item-text="title"
              v-model="chartFilterDefault"
              label="Show Data For"
              v-on:change="filterByChartColumn"
            ></v-select>
          </v-col>
        </v-row>
        <Bar v-if="chartMode" :data="chartData"></Bar>
      </template> -->
    </v-layout>
    <div class="text-center pt-2">
      <v-pagination
        v-if="tickets.length > 32"
        v-model="page"
        :length="pageCount"
      ></v-pagination>
    </div>
  </div>
</template>

<script>
// var _ = require('lodash');
import {targetURL} from "../global/config";
// import Bar from "../views/charts/Bar.vue";
const axios = require("axios").default;
export default {
  name: "cashflow",
  data() {
    return {
      initialLoad:true,
      url:targetURL.LOCAL,
      overalls: {
        deposit_users: null,
        deposit_number: null,
        deposit_sum: null,
        withdraw_users: null,
        withdraw_number: null,
        withdraw_sum: null,
        promo_users:null,
        promo_number:null,
        promo_sum:null,
        std_balance_start:null,
        std_balance_end:null
      },
      menu:false,
      dates:[],
      otherLists: {
        showYear: true,
        showMonth: false,
        showCalendar:false,
      },
      error: false,
      todayDateFile: new Date().toISOString() + ".xls",
      json_fields: {},
      json_data: [],
      json_meta: [
        [
          {
            key: "charset",
            value: "utf-8",
          },
        ],
      ],
      pagination: {
        sortBy: "name",
      },
      responsiveTable: false,
      isMobile: false,
      page: 1,
      pageCount: 0,
      itemsPerPage: 32,
      loadTable: true,
      monthDefault: 0,
      yearDefault: 2021,
      methodDefault: 0,
      periodDefault: 0,
      methods: [
        {
          id: 0,
          title: "All",
        },
        {
          id: 1,
          title: "Dobri Komšija",
        },
        {
          id: 2,
          title: "Shops",
        },
        {
          id: 3,
          title: "Credit Card",
        },
        {
          id: 4,
          title: "iPay",
        },
        {
          id: 5,
          title: "Bank Transfer",
        },
      ],
      periods: [
        {
          id: 0,
          title: "Per Year",
        },
        {
          id: 1,
          title: "Per Month",
        },
        {
          id: 2,
          title: "Weekend",
        },
        {
          id: 3,
          title: "Today",
          disabled:true
        },
      ],
      months: [
        {
          id: 0,
          title: "All",
          from: "-01-01",
          to: "-12-31",
        },
        {
          id: 1,
          from: "-01-01",
          to: "-01-31",
          title: "January",
        },
        {
          from: "-02-01",
          to: "-02-"+this.getLastDayOfMonth(1), //1 - februar
          id: 2,
          title: "February",
        },
        {
          from: "-03-01",
          to: "-03-31",
          id: 3,
          title: "March",
        },
        {
          from: "-04-01",
          to: "-04-30",
          id: 4,
          title: "April",
        },
        {
          from: "-05-01",
          to: "-05-31",
          id: 5,
          title: "May",
        },
        {
          from: "-06-01",
          to: "-06-30",
          id: 6,
          title: "June",
        },
        {
          from: "-07-01",
          to: "-07-31",
          id: 7,
          title: "July",
        },
        {
          from: "-08-01",
          to: "-08-31",
          id: 8,
          title: "August",
        },
        {
          from: "-09-01",
          to: "-09-30",
          id: 9,
          title: "September",
        },
        {
          from: "-10-01",
          to: "-10-31",
          id: 10,
          title: "October",
        },
        {
          from: "-11-01",
          to: "-11-30",
          id: 11,
          title: "November",
        },
        {
          from: "-12-01",
          to: "-12-31",
          id: 12,
          title: "December",
        },
      ],
      years: [
        {
          id: 2021,
          title: "2021",
        },
        {
          id: 2020,
          title: "2020",
        },
        {
          id: 2019,
          title: "2019",
        },
        {
          id: 2018,
          title: "2018",
        },
      ],
      search: "",
      tiketi: [],
      filters: {
        month: 0,
        year: 2021,
        method: 0,
        period: 0
      },
    };
  },
  methods: {
    getLastDayOfMonth(month){
      //0 - januar
      var d = new Date(new Date().getFullYear(), month + 1, 0);
      return d.getDate()
    },
    fromCurrencyToFloat(value) {
      return parseFloat(value.replace(/,/g, ""));
    },
    convertToReadableNumber(value) {
      let num = this.convertToCurrency(value);
      return num.substring(0, num.length - 3);
    },
    convertToCurrency(value) {
      const formatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        minimumFractionDigits: 2,
      });
      return formatter.format(value).replace("$", "");
    },
    formatTicket(response) {
      if (Object.keys(response.data.tiket).length != 0) {
        this.tickets = response.data.tiket;
        this.tickets.forEach((ticket) => {
          ticket["deposit_users"] = this.convertToReadableNumber(ticket["deposit_users"]);
          ticket["deposit_number"] = this.convertToReadableNumber(ticket["deposit_number"]);
          ticket["deposit_sum"] = this.convertToCurrency(ticket["deposit_sum"]);
          ticket["withdraw_users"] = this.convertToReadableNumber(ticket['withdraw_users']);
          ticket["withdraw_number"] = this.convertToReadableNumber(ticket['withdraw_number']);
          ticket["withdraw_sum"] = this.convertToCurrency(ticket["withdraw_sum"]);
          ticket["promo_users"] = this.convertToReadableNumber(0);
          ticket["promo_number"] = this.convertToReadableNumber(0);
          ticket["promo_sum"] = this.convertToCurrency(0);
          ticket["std_balance_start"] = this.convertToCurrency(0);
          ticket["std_balance_end"] = this.convertToCurrency(0);
        });
        this.createOveralls();
        this.mapStakes();
      } else {
        this.tickets = [];
      }
      this.json_data = this.tickets;
      // let a = this.prepareForExcel(_.cloneDeep(this.tickets))
    },
    prepareForExcel(tickets){
      for(let i = 0; i<tickets.length; i++){
        for(var key in tickets[i]){
          if(key!='Opseg'){
            tickets[i][key]=parseFloat(this.convertToCleanFloat(tickets[i][key]))
          }
        }
      }
      return tickets;
    },
    isDayFiltering() {
      return (
        this.tickets.filter((x) => x.Opseg.toString().includes("-")).length > 0
      );
    },
    mapStakes() {
      this.tickets.sort((a, b) => (a.Opseg > b.Opseg ? 1 : -1));
      if (!this.isDayFiltering()) {
        let months = [
          "January",
          "February",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
        ];

        this.tickets.forEach((tiket) => {
          if(this.filters.period==1)
          tiket["Opseg"] = months[tiket["Opseg"]-1];
        });
      } 
    },
    createOveralls() {
      //c - stands for cumulative
      let cDepositSum = this.tickets.reduce(
        (a, b) => a + this.fromCurrencyToFloat(b["deposit_sum"]),
        0
      );
      let cWithdrawSum = this.tickets.reduce(
        (a, b) => a + this.fromCurrencyToFloat(b["withdraw_sum"]),
        0
      );
      
      this.overalls.deposit_sum = this.convertToReadableNumber(cDepositSum);
      this.overalls.withdraw_sum = this.convertToReadableNumber(cWithdrawSum);
    },
    determineURL() {
      let path = window.origin;
      if (path.includes("localhost")) {
        this.url = targetURL.LOCAL;
      } else {
        this.url = targetURL.SERVER;
      }
  },
    onResize() {
      if (window.innerWidth < 769) this.isMobile = true;
      else this.isMobile = false;
    },
    filterByPeriod(criteria) {
      this.dates = [];
      this.showOtherLists(criteria);
      this.filters.period = criteria;
    },
    filterByMethod(criteria) {
      this.filters.method = criteria;
    },
    filterByMonth(criteria) {
      this.filters.month = criteria;
    },
    filterByYear(criteria) {
      this.filters.year = criteria;
    },
    showOtherLists(period) {
      switch (period) {
        case 0:
          this.otherLists.showYear = true;
          this.otherLists.showMonth = false;
          this.otherLists.showCalendar = false;
          break;
        case 1:
          this.otherLists.showYear = false;
          this.otherLists.showMonth = true;
          this.otherLists.showCalendar = false;
          break;
        case 2:
          this.otherLists.showYear = false;
          this.otherLists.showMonth = false;
          this.otherLists.showCalendar = true;
        break;
        default:
          this.otherLists.showYear = false;
          this.otherLists.showMonth = false;
          this.otherLists.showCalendar = false;
          break;
      }
    },
    //Formatting json
    formatJson(filterVal, jsonData) {
      return jsonData.map((v) => filterVal.map((j) => v[j]));
    },
    getData() {
      this.initialLoad = false;
      this.loadTable = true;
      this.tickets = [];
      let obj = this.prepareData();
      this.emptyObject(this.overalls);
      axios
        .post(this.url+"/api/Cashflow", obj)
        .then((response) => {
          this.formatTicket(response);
          this.loadTable = false;
        });
    },
    isNegative(val) {
      return val == null || val == "";
    },
    emptyObject(obj) {
      for (const [key] of Object.entries(obj)) {
        obj[key] = null;
      }
    },
    convertToCleanFloat(num) {
      return num.replace("$", "").replace(/,/g, "");
    },
    prepareData(){
      let ADDITIONAL = 0;
      if(this.filters.month==0 || this.filters.month==12)
      ADDITIONAL = 1;

      let obj = {
        period:this.filters.period,
        paymentMethod:this.filters.method
      }
      if(obj.period==0){
        obj.year = this.filters.year
        obj.dates = null
        obj.monthFrom = null
        obj.monthTo = null
      }
      if(obj.period==1){
        obj.monthFrom = new Date().getFullYear()+this.months.filter(x=>x.id==this.filters.month)[0].from
        obj.monthTo = new Date().getFullYear()+ADDITIONAL+this.months.filter(x=>x.id==this.filters.month)[0].to
        obj.year = null
        obj.dates = null
      }
      if(obj.period==2){
        obj.dates = this.dates
        obj.monthFrom = null
        obj.monthTo = null
        obj.year = null
      }

      return obj;
    }
  },
  computed: {
    tickets: {
      get() {
        let filtered;
        filtered = this.tiketi;
        return filtered;
      },
      set(value) {
        this.tiketi = value;
      },
    },
    headers() {
      return [
        {
          text: "Users",
          align: "start",
          value: "deposit_users",
        },
        {
          text: "Number",
          value: "deposit_number",
        },
        {
          text: "Sum",
          value: "deposit_sum",
        },
        {
          text: "Users",
          value: "withdraw_users",
        },
        {
          text: "Number",
          value: "withdraw_number",
        },
        {
          text: "Sum",
          value: "withdraw_sum",
        },
        {
          text: "Users",
          value: "promo_users",
        },
        {
          text: "Number",
          value: "promo_number",
        },
        {
          text: "Sum",
          value: "promo_sum",
        },
        {
          text: "Start",
          value: "std_balance_start",
        },
        {
          text: "End",
          value: "std_balance_end",
        }
      ];
    },
  },
  created() {
    this.determineURL();
    this.tickets = [];
    // this.loadTable = true;
    // axios
    //   .get(this.url+"/api/Cashflow")
    //   .then((response) => {
    //     this.formatTicket(response);
    //     this.loadTable = false;
    //   })
    //   .catch((e) => {
    //     console.error(e.message);
    //   });
  },
};
</script>

<style>

.from .v-input__slot,
.to .v-input__slot {
  width: 50px !important;
}
.to .v-text-field__slot label:first-child {
  padding-left: 41px;
}
.cashflowMobile {
  color: #333;
}
.v-toolbar__content {
  background-color: #225e0d !important;
}
@media screen and (min-width: 768px) {
  #report2 table {
    border-top: 1px solid black;
  }
  #report2 .mainHeader:nth-child(7),
  #report2 .mainHeader:nth-child(13),
    #report2 .mainHeader:nth-child(12)
  {
    border-right: 1px solid black
  }

  #report2 .mainHeader:nth-child(11){
    border-left:1px solid black
  }

  #report2 .mainHeader:nth-child(2) {
    border-left: 1px solid black;
  }
  #report2 .mainHeader:nth-child(4) {
    border-right: 1px solid black;
  }
  #report2 table td + td {
    border-left: 1px solid black;
  }
  #report2 table td:last-child{
    border-right:1px solid black;
  }
  #report2 table{
    border-bottom:1px solid black
  }
}
@media screen and (max-width: 768px) {
  .desktop,
  .v-data-table-header tr {
    height: 55px !important;
  }
  .cashflowMobile table tr {
    max-width: 100%;
    position: relative;
    display: block;
    height: 355px;
  }

  .cashflowMobile table tr:nth-child(odd) {
    border-left: 6px solid rgb(48, 170, 103);
  }

  .cashflowMobile table tr:nth-child(even) {
    border-left: 6px solid rgb(174, 179, 179);
  }

  .cashflowMobile table tr td {
    display: flex;
    width: 100%;
    /* border-bottom: 1px solid #f5f5f5; */
    height: auto;
    padding: 10px;
  }

  .cashflowMobile table tr td ul li:before {
    content: attr(data-label);
    padding-right: 0.5em;
    text-align: left;
    display: block;
    color: #999;
  }
  .v-datatable__actions__select {
    width: 50%;
    margin: 0px;
    justify-content: flex-start;
  }
  .cashflowMobile .theme--light tbody tr:hover:not(.v-datatable__expand-row) {
    background: transparent;
  }
}
#mobileRow .flex-content {
  padding: 0;
  margin: 0;
  list-style: none;
  display: flex;
  flex-wrap: wrap;
  width: 100%;
}

#mobileRow .flex-item {
  padding: 5px;
  width: 50%;
  height: 40px;
  font-weight: bold;
}
</style>