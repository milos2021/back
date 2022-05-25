<template>
  <div>
    <v-container fluid>
      <v-row align="center" class="mtop12">
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
        <v-col cols="12" sm="6">
          <v-dialog
            ref="dialog"
            v-model="modal"
            :return-value.sync="dates"
            persistent
            min-width="auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                v-model="dates"
                multiple
                label="Select dates"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="attrs"
                v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
              v-model="dates"
              multiple
              dark
              chips
              no-title
              scrollable
            >
              <v-spacer></v-spacer>

              <v-btn text color="primary" @click="$refs.dialog.save(dates)">
                OK
              </v-btn>
              <v-btn text color="primary" @click="modal = false"> Close </v-btn>
              <v-btn text color="primary" @click="dates = []"> Clear </v-btn>
            </v-date-picker>
          </v-dialog>
          <div class="text-center">
            <v-snackbar v-model="snackbar" :timeout="timeout">
              {{ errorText }}

              <template v-slot:action="{ attrs }">
                <v-btn
                  color="blue"
                  text
                  v-bind="attrs"
                  @click="snackbar = false"
                >
                  Close
                </v-btn>
              </template>
            </v-snackbar>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <v-container fluid>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-btn
            color="primary"
            elevation="2"
            disabled
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
            v-if="!initialLoad && tiketi.length > 0"
          >
            <img
              src="@/assets/excel.png"
              style="
                margin-top: -8px;
                margin-left: 3px;
                width: 40px;
                cursor: pointer;
              "
            />
          </export-excel>
        </v-col>
      </v-row>
    </v-container>
    <v-layout
      v-if="!initialLoad"
      v-resize="onResize"
      column
      style="padding-top: 56px"
    >
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
          <tr style="text-align: center">
            <th></th>
            <th
              colspan="3"
              style="
                border-left: 1px solid black;
                border-right: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              Deposit
            </th>
            <th
              colspan="3"
              style="
                border-right: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              Withdraw
            </th>
            <th
              colspan="3"
              style="
                border-right: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              Promo Achivement
            </th>
            <th
              colspan="2"
              style="
                border-right: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              Standard Balance
            </th>
            <th colspan="3" style="border-bottom: 1px solid black">
              Promo Balance
            </th>
          </tr>
          <tr style="text-align: center">
            <th class="mainHeader"></th>
            <th
              class="mainHeader"
              style="text-align: left; padding-left: 15px; padding-top: 10px"
              v-for="head in props.headers"
              :key="head.value"
            >
              {{ head.text.toUpperCase() }}
            </th>
          </tr>
          <tr style="text-align: center">
            <th
              style="
                text-align: left;
                padding-left: 15px;
                padding-bottom: 5px;
                border-right: 1px solid black;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              Overall
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.deposit_users }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.deposit_number }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.deposit_sum }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.withdraw_users }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.withdraw_number }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.withdraw_sum }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.promo_users }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.promo_number }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.promo_sum }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.std_balance_start }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.std_balance_end }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.promo_balance_start }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.promo_balance_end }}
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
            <td class="text-xs-right">{{ item.promo_balance_start }}</td>
            <td class="text-xs-right">{{ item.promo_balance_end }}</td>
          </tr>
          <tr id="mobileRow" v-else>
            <td
              style="
                border-top: thin solid rgba(0, 0, 0, 0.12);
                border-bottom: none;
              "
            >
              <ul class="flex-content">
                <li class="flex-item" data-label="RANGE">
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
                <li class="flex-item" data-label="P-START">
                  {{ item.promo_balance_start }}
                </li>
                <li class="flex-item" data-label="P-END">
                  {{ item.promo_balance_end }}
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
var _ = require("lodash");
import { targetURL } from "../global/config";
// import Bar from "../views/charts/Bar.vue";
const axios = require("axios").default;
export default {
  name: "cashflow",
  data() {
    return {
      snackbar: false,
      errorText: "You can select up to 4 days",
      timeout: 3000,
      initialLoad: true,
      url: targetURL.LOCAL,
      overalls: {
        deposit_users: null,
        deposit_number: null,
        deposit_sum: null,
        withdraw_users: null,
        withdraw_number: null,
        withdraw_sum: null,
        promo_users: null,
        promo_number: null,
        promo_sum: null,
        std_balance_start: null,
        std_balance_end: null,
        promo_balance_start: null,
        promo_balance_end: null,
      },
      menu: false,
      dates: [],
      modal: false,
      otherLists: {
        showYear: true,
        showMonth: false,
        showCalendar: false,
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
          disabled:true
        },
        {
          id: 2,
          title: "Shops",
        },
        {
          id: 3,
          title: "Credit Card",
          disabled:true
        },
        {
          id: 4,
          title: "iPay",
          disabled:true
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
          disabled: true,
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
          to: "-02-" + this.getLastDayOfMonth(1), //1 - februar
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
        period: 0,
      },
    };
  },
  methods: {
    getLastDayOfMonth(month) {
      //0 - januar
      var d = new Date(new Date().getFullYear(), month + 1, 0);
      return d.getDate();
    },
    fromCurrencyToFloat(value) {
      value = value.toString();
      return parseFloat(value.replace(/,/g, ""));
    },
    convertToReadableNumber(value) {
      let num = this.convertToCurrency(value);
      return num.substring(0, num.length - 3);
    },
    convertToCurrency(value) {
      if (value == "/") {
        return value;
      }
      const formatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        minimumFractionDigits: 2,
      });
      return formatter.format(value).replace("$", "");
    },
    formatTicket(response) {
      let serverData = _.cloneDeep(response.data.tiket);
      response.data.tiket = response.data.tiket.filter((x) => x.Opseg);
      if (Object.keys(response.data.tiket).length != 0) { //bez null Opsega
        this.tickets = response.data.tiket;
        this.tickets.forEach((ticket) => {
          this.formatData(ticket);
          ticket["std_balance_start"] = this.convertToCurrency(
            ticket["std_balance"]
          );
          ticket["std_balance_end"] = "/";
          ticket["promo_balance_start"] = this.convertToCurrency(
            ticket["promo_balance"]
          );
          ticket["promo_balance_end"] = "/";
        });
        this.createEnds(null, null, serverData);
      } else {
        if (serverData.filter((x) => !x.Opseg).length > 0)
          this.createEnds(null, null, serverData);
        else this.tickets = [];
      }
      this.json_data = this.tickets;
      // let a = this.prepareForExcel(_.cloneDeep(this.tickets))
    },
    formatData(ticket, zero) {
      ticket["deposit_users"] = this.convertToReadableNumber(
        zero ? 0 : ticket["deposit_users"]
      );
      ticket["deposit_number"] = this.convertToReadableNumber(
        zero ? 0 : ticket["deposit_number"]
      );
      ticket["deposit_sum"] = this.convertToCurrency(
        zero ? 0 : ticket["deposit_sum"]
      );
      ticket["withdraw_users"] = this.convertToReadableNumber(
        zero ? 0 : ticket["withdraw_users"]
      );
      ticket["withdraw_number"] = this.convertToReadableNumber(
        zero ? 0 : ticket["withdraw_number"]
      );
      ticket["withdraw_sum"] = this.convertToCurrency(
        zero ? 0 : ticket["withdraw_sum"]
      );
      ticket["promo_users"] = this.convertToReadableNumber(
        zero ? 0 : ticket["promo_users"]
      );
      ticket["promo_number"] = this.convertToReadableNumber(
        zero ? 0 : ticket["promo_number"]
      );
      ticket["promo_sum"] = this.convertToCurrency(
        zero ? 0 : ticket["promo_sum"]
      );
    },
    createEnds(s, p, data = null) {
      if (!data) {
        for (let i = 0; i < this.tickets.length; i++) {
          if (i < this.tickets.length - 1) {
            this.tickets[i]["std_balance_end"] = this.tickets[i + 1][
              "std_balance_start"
            ];
            this.tickets[i]["promo_balance_end"] = this.tickets[i + 1][
              "promo_balance_start"
            ];
          }

          if (i == this.tickets.length - 1) {
            this.tickets[i]["std_balance_end"] = this.convertToCurrency(s);
            this.tickets[i]["promo_balance_end"] = this.convertToCurrency(p);
          }
        }
      } else {
        this.showDataForPastBalances(data);
        if(this.filters.period==2){
        for (let i = 0; i < data.length; i++) {
          for (let j = 0; j < data.length; j++) {
            if (
              new Date(data[i].Opseg).setDate(
                new Date(data[i].Opseg).getDate() + 1
              ) === new Date(data[j].BalanceOpseg).getTime()
            ) {
              this.tickets.filter((x) => x.Opseg == data[i].Opseg)[0][
                "std_balance_end"
              ] = this.convertToCurrency(data[j]["std_balance"]);
              this.tickets.filter((x) => x.Opseg == data[i].Opseg)[0][
                "promo_balance_end"
              ] = this.convertToCurrency(data[j]["promo_balance"]);
            }
          }
        }
        }


        this.createOveralls();
        this.mapStakes();
      }
    },
    showDataForPastBalances(data) {
      console.log(data, this.dates);
      if (this.filters.period == 2) {
        for (let i = 0; i < data.length; i++) {
          for (let j = 0; j < this.dates.length; j++) {
            if (
              data[i].BalanceOpseg == this.dates[j] &&
              data[i].Opseg == null
            ) {
              console.log("OLA");
              data[i].Opseg = data[i].BalanceOpseg;
              data[i]["std_balance_start"] = this.convertToCurrency(
                data[i]["std_balance"]
              );
              data[i]["promo_balance_start"] = this.convertToCurrency(
                data[i]["promo_balance"]
              );
              this.formatData(data[i], true);
              this.tickets.push(data[i]);
            }
          }
        }
      }
      if (this.filters.period == 0){
        let mergedData = _.cloneDeep(data[0]);
        mergedData['std_balance']="/";
        mergedData['promo_balance']="/";
        console.log(data)
        for(let i=0; i<data.length;i++){
          if(data[i].BalanceOpseg==this.filters.year+"-01-01"){
            mergedData['std_balance_start']=this.convertToCurrency(data[i]['std_balance']);
            mergedData['promo_balance_start']=this.convertToCurrency(data[i]['promo_balance']);
          }
          if(data[i].BalanceOpseg==this.filters.year+"-12-31"){
            mergedData['std_balance_end']=this.convertToCurrency(data[i]['std_balance']);
            mergedData['promo_balance_end']=this.convertToCurrency(data[i]['promo_balance']);
          }
        }
        if(data.filter(x=>x.Opseg).length==0){
            mergedData.Opseg = this.filters.year;
            if(!mergedData['std_balance_start']){
              mergedData['std_balance_start']="/";
            }
            if(!mergedData['promo_balance_start']){
              mergedData['promo_balance_start']="/";
            }
            this.formatData(mergedData, true);
            console.log("AAA")
            this.tickets.push(mergedData)
        }
        console.log(this.tickets)
      }
      if(this.filters.period==1){
        if(this.filters.month!=0){
        let mergedData = _.cloneDeep(data[0]);
        mergedData['std_balance']="/";
        mergedData['promo_balance']="/";
        console.log(data)
        console.log(_.cloneDeep(this.tickets))
        for(let i=0; i<data.length;i++){
          if(data[i].BalanceOpseg==new Date().getFullYear()+"-"+this.getMonth(this.filters.month)+"-01"){
            mergedData['std_balance_start']=this.convertToCurrency(data[i]['std_balance']);
            mergedData['promo_balance_start']=this.convertToCurrency(data[i]['promo_balance']);
          }
          if(data[i].BalanceOpseg==new Date().getFullYear()+"-"+this.getMonth(this.filters.month)+"-"+this.getLastDayOfMonth(this.filters.month-1)){
            mergedData['std_balance_end']=this.convertToCurrency(data[i]['std_balance']);
            mergedData['promo_balance_end']=this.convertToCurrency(data[i]['promo_balance']);
          }
        }
            mergedData.Opseg = this.filters.month;
            console.log(mergedData)
            if(!mergedData['std_balance_start']){
              mergedData['std_balance_start']="/";
            }
            if(!mergedData['promo_balance_start']){
              mergedData['promo_balance_start']="/";
            }
            if(!mergedData['std_balance_end']){
              mergedData['std_balance_end']="/";
            }
            if(!mergedData['promo_balance_end']){
              mergedData['promo_balance_end']="/";
            }

            if(data.filter(x=>x.Opseg).length>0){
            this.formatData(data[0]);
            this.tickets = [];
            this.tickets.push({...mergedData, ...data[0]})
            } else {
            this.formatData(mergedData, true);
            this.tickets = [];
            this.tickets.push(mergedData)
            }
            console.log("AAA")

        }
      }
    },
    prepareForExcel(tickets) {
      for (let i = 0; i < tickets.length; i++) {
        for (var key in tickets[i]) {
          if (key != "Opseg") {
            tickets[i][key] = parseFloat(
              this.convertToCleanFloat(tickets[i][key])
            );
          }
        }
      }
      return tickets;
    },
    isDayFiltering() {
      return (
        this.tickets.filter((x) =>
          x.Opseg ? x.Opseg.toString().includes("-") : false
        ).length > 0
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
          if (this.filters.period == 1)
            tiket["Opseg"] = months[tiket["Opseg"] - 1];
        });
      }
      if (this.filters.period == 2) {
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
          let datePrep = new Date(tiket["Opseg"]);
          tiket["Opseg"] =
            datePrep.getDate() +
            ". " +
            months[datePrep.getMonth()] +
            " " +
            datePrep.getFullYear() +
            ".";
        });
      }
      console.log(_.cloneDeep(this.tickets));
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
      console.log("O");
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
      // if (this.dates.length > 4) {
      //   this.snackbar = true;
      //   this.modal = true;
      //   return;
      // }
      if (this.dates.length > 0 || this.filters.period != 2) {
        this.initialLoad = false;
        this.loadTable = true;
        this.tickets = [];
        let obj = this.prepareData();
        this.emptyObject(this.overalls);
        axios.post(this.url + "/api/Cashflow", obj).then((response) => {
          this.formatTicket(response);
          this.loadTable = false;
        });
      }
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
    prepareData() {


      let obj = {
        period: this.filters.period,
        paymentMethod: this.filters.method,
      };
      if (obj.period == 0) {
        let balanceMargins = [
          this.filters.year + "-01-01",
          this.filters.year + "-12-31",
        ];
        obj.year = this.filters.year;
        obj.dates = null;
        obj.monthFrom = null;
        obj.monthTo = null;
        obj.balanceTo = null;
        obj.balanceDates = balanceMargins;
      }
      if (obj.period == 1) {
        console.log(this.filters.month);
        obj.monthFrom =
          new Date().getFullYear() +
          this.months.filter((x) => x.id == this.filters.month)[0].from;
        obj.monthTo =
          new Date().getFullYear() +
          this.months.filter((x) => x.id == this.filters.month)[0].to;

        if(this.filters.month!=0){
            obj.balanceDates=[new Date().getFullYear()+"-"+this.getMonth(this.filters.month)+"-01", new Date().getFullYear()+"-"+this.getMonth(this.filters.month)+"-"+this.getLastDayOfMonth(this.filters.month-1)];
        } else {
          let balanceDates = [];
             for(let i=1; i<=12; i++){
               balanceDates.push(new Date().getFullYear()+"-"+this.getMonth(i)+"-01");
               balanceDates.push(new Date().getFullYear()+"-"+this.getMonth(i)+"-"+this.getLastDayOfMonth(i-1));
             }
             obj.balanceDates = balanceDates
        }

        obj.balanceTo=null;
        obj.year = null;
        obj.dates = null;
      }
      if (obj.period == 2) {
        obj.dates = this.dates;
        obj.balanceDates = this.prepareDates();
        obj.balanceTo = 1;
        obj.monthFrom = null;
        obj.monthTo = null;
        obj.year = null;
      }

      return obj;
    },
    getMonth(num) {
      if (num < 10) {
        return "0" + num;
      } else {
        return num;
      }
    },
    prepareDates() {
      this.dates = this.dates.sort((a, b) => new Date(a) - new Date(b));
      console.log(this.dates);
      let balanceDates = _.cloneDeep(this.dates);
      for (let i = 0; i < this.dates.length; i++) {
        balanceDates.push(this.getNextDay(this.dates[i]));
      }
      balanceDates = balanceDates.sort((a, b) => new Date(a) - new Date(b));
      balanceDates = [...new Set(balanceDates)];
      return balanceDates;
    },
    getNextDay(day) {
      let lastDay = new Date(day);
      let nextDay = new Date(lastDay).setDate(lastDay.getDate() + 1);
      return this.convertToDate(nextDay);
    },
    convertToDate(date) {
      var d = new Date(date),
        month = "" + (d.getMonth() + 1),
        day = "" + d.getDate(),
        year = d.getFullYear();

      if (month.length < 2) month = "0" + month;
      if (day.length < 2) day = "0" + day;

      return [year, month, day].join("-");
    },
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
        },
        {
          text: "Start",
          value: "promo_balance_start",
        },
        {
          text: "End",
          value: "promo_balance_end",
        },
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
.v-dialog {
  width: 290px !important;
}
.mtop12 {
  margin-top: 9px;
}
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
  #report2 .mainHeader:nth-child(11),
  #report2 .mainHeader:nth-child(13),
  #report2 .mainHeader:last-child {
    border-right: 1px solid black;
  }
  #report2 .mainHeader:nth-child(11),
  #report2 .mainHeader:nth-child(13) {
    border-left: 1px solid black;
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
  #report2 table {
    border-bottom: 1px solid black;
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

.v-data-table__wrapper {
  overflow: hidden;
  background: azure;
}
</style>