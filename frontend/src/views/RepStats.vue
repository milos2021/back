<template>
  <div>
    <v-container v-if="!chartMode || initialLoad" fluid>
      <v-row align="center" class="mtop12">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            :disabled="disableList.month"
            :items="months"
            item-value="id"
            item-text="title"
            v-model="monthDefault"
            label="Month"
            v-on:change="filterByMonth"
          ></v-select>
        </v-col>
      </v-row>
      <v-row align="center">
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
      <v-row align="center" style="display: none">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            :items="channels"
            item-value="id"
            item-text="title"
            :disabled="isChannelDisabled"
            v-model="channelDefault"
            label="Channel"
            v-on:change="filterByChannel"
          ></v-select>
        </v-col>
      </v-row>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            :items="slipTypes"
            item-value="id"
            item-text="title"
            v-model="slipTypeDefault"
            label="Slip Type"
            v-on:change="filterBySlipType"
          ></v-select>
        </v-col>
      </v-row>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            :items="aspects"
            item-value="id"
            item-text="title"
            v-model="aspectDefault"
            label="Aspect"
            v-on:change="filterByAspect"
          ></v-select>
        </v-col>
        <v-col class="d-flex" cols="12" sm="6" v-if="filters.aspect == 0">
          <v-text-field
            v-model="ranges.from"
            @keyup.native="checkIfEligible"
            @change.native="checkIfEligible"
            min="20"
            type="number"
            class="from"
            label="("
          ></v-text-field>
          <v-text-field
            v-model="ranges.to"
            @keyup.native="checkIfEligible"
            @change.native="checkIfEligible"
            min="0"
            type="number"
            class="to"
            id="to"
            label="]"
          ></v-text-field>
          <!-- <v-alert type="error" v-if="error">
            Error
          </v-alert> -->
        </v-col>
      </v-row>
    </v-container>
    <v-container v-if="!chartMode || initialLoad" fluid>
      <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-tooltip v-if="errorMessage" top>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="error"
                elevation="2"
                depressed
                v-bind="attrs"
                v-on="on"
                v-on:click="getData"
                >Range Error</v-btn
              >
            </template>
            <span>{{ errorMessage }}</span>
          </v-tooltip>
          <v-btn
            v-if="!errorMessage"
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
          <img
            v-if="
              !chartMode &&
              chartData &&
              !ranges.from &&
              !ranges.to &&
              !initialLoad &&
              tiketi.length > 0
            "
            src="@/assets/charts2.png"
            style="height: 35px; margin-top: 2px; cursor: pointer"
            @click="switchMode"
          />
          <img
            v-if="chartMode && !initialLoad"
            src="@/assets/table.png"
            style="height: 40px; margin-top: -2px; cursor: pointer"
            @click="switchMode"
          />
        </v-col>
      </v-row>
    </v-container>
    <v-layout
      v-if="!initialLoad"
      v-resize="onResize"
      column
      :style="[
        !chartMode ? { 'padding-top': '56px' } : { 'padding-top': 'inherit' },
      ]"
    >
        <p v-if="reportGenTime" class="reportTime">Report generated at: {{reportGenTime}}</p>
      <v-data-table
        v-if="!chartMode"
        id="report4"
        :headers="headers"
        :hide-default-header="!isMobile"
        :page.sync="page"
        :items-per-page="itemsPerPage"
        hide-default-footer
        :items="tickets"
        :class="{ mobile: isMobile }"
        item-key="name"
        :loading="loadTable"
        @page-count="pageCount = $event"
        no-data-text="No data"
        loading-text="Data is loading..."
      >
        <template v-if="!isMobile" v-slot:header="{ props }">
          <tr>
            <th style="background:lightblue"></th>
            <th
              style="
                border-left: 1px solid black;
                border-right: 1px solid black;
                text-align: center;
                background:lightblue;
              "
            >
              Turnover
            </th>
            <th
              colspan="7"
              style="border-right: 1px solid black; text-align: center; background:red; color:white"
            >
              Winnings
            </th>
            <th colspan="4" style="text-align: center; background:yellowgreen">GGR Margin</th>
          </tr>
          <tr>
            <th
              class="mainHeader"
              style="text-align: left; padding-left: 15px; padding-top: 10px"
              v-for="head in props.headers"
              :key="head.value"
            >
              {{ head.text.toUpperCase() }}
            </th>
          </tr>
          <tr style="background:lightgoldenrodyellow;">
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
              {{ overalls.sumbet }}
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
              {{ overalls.sumwin }}
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
              {{ overalls.regular }}
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
              {{ overalls.ctrbRegular }}
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
              {{ overalls.bonus }}
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
              {{ overalls.ctrbBonus }}
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
              {{ overalls.cashback }}
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
              {{ overalls.ctrbCashback }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.ggrRegular }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.ggrRegularMargin }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.ggr }}
            </th>
            <th
              style="
                text-align: left;
                padding-left: 15px;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            >
              {{ overalls.ggrMargin }}
            </th>
          </tr>
        </template>
        <template v-slot:item="{ item }">
          <tr v-if="!isMobile">
            <td>{{ item.Opseg }}</td>
            <td class="text-xs-right">{{ item.SumBet }}</td>
            <td class="text-xs-right">{{ item.SumWin }}</td>
            <td class="text-xs-right">{{ item.SumRegularWin }}</td>
            <td class="text-xs-right">{{ item.CtrbRegular }}</td>
            <td class="text-xs-right">{{ item.SumBonusWin }}</td>
            <td class="text-xs-right">{{ item.CtrbBonus }}</td>
            <td class="text-xs-right">{{ item.SumCashbackWin }}</td>
            <td class="text-xs-right">{{ item.CtrbCashback }}</td>
            <td class="text-xs-right">{{ item.GgrRegular }}</td>
            <td class="text-xs-right">{{ item.GgrRegularMargin }}</td>
            <td class="text-xs-right">{{ item.Ggr }}</td>
            <td class="text-xs-right">{{ item.GgrMargin }}</td>

          </tr>
          <tr id="mobileRow" v-else>
            <td
              style="
                border-top: thin solid rgba(0, 0, 0, 0.12);
                border-bottom: none;
              "
            >
              <ul class="flex-content">
                <li class="flex-item" data-label="PERIOD">
                  {{ item.Opseg }}
                </li>
                <li class="flex-item" data-label="ΣBET">
                  {{ item.SumBet }}
                </li>
                <li class="flex-item" data-label="ΣWIN">
                  {{ item.SumWin }}
                </li>
                <li class="flex-item" data-label="Regular">
                  {{ item.SumRegularWin }}
                </li>
                <li class="flex-item" data-label="Ctrb">
                  {{ item.CtrbRegular }}
                </li>
                <li class="flex-item" data-label="Bonus">
                  {{ item.SumBonusWin }}
                </li>
                <li class="flex-item" data-label="Ctrb">
                  {{ item.CtrbBonus }}
                </li>
                <li class="flex-item" data-label="Cashback">
                  {{ item.SumCashbackWin }}
                </li>
                <li class="flex-item" data-label="Ctrb">
                  {{ item.CtrbCashback }}
                </li>
                <li class="flex-item" data-label="ΣGGR (regular)">
                  {{ item.GgrRegular }}
                </li>
                <li class="flex-item" data-label="Margin">
                  {{ item.GgrRegularMargin }}
                </li>
                <li class="flex-item" data-label="ΣGGR">
                  {{ item.Ggr }}
                </li>
                <li class="flex-item" data-label="Margin">
                  {{ item.GgrMargin }}
                </li>
              </ul>
            </td>
          </tr>
        </template>
      </v-data-table>
      <template v-if="chartMode">
        <v-row style="margin-top: 5px; margin-top: 10px" align="center">
          <!--class="chartsMode"-->
          <v-col id="sortChart" class="d-flex" cols="12" lg="4" md="4" sm="12">
            <v-select
              :items="chartFilterData"
              item-value="id"
              item-text="title"
              v-model="chartFilterDefault"
              v-on:change="filterByChartColumn"
            ></v-select>
          </v-col>
        </v-row>
        <Bar
          v-if="chartMode"
          :data="chartData"
          :style="[
            chartMode
              ? { width: '100%', height: '100%' }
              : { width: 'auto', height: 'auto' },
          ]"
        ></Bar>
        <img
          v-if="chartMode && !initialLoad && orientationMode != 'landscape'"
          src="@/assets/table.png"
          style="width: 65px; margin: 0 auto; cursor: pointer"
          @click="switchMode"
        />
      </template>
    </v-layout>
    <div class="text-center pt-2" v-if="!chartMode || initialLoad">
      <v-pagination
        v-if="tickets.length > 32"
        v-model="page"
        :length="pageCount"
      ></v-pagination>
    </div>
  </div>
</template>

<script>
import OrientationService from "../services/orientation.service.js";

const axios = require("axios").default;
import { targetURL } from "../global/config";
import Bar from "../views/charts/Bar.vue";
export default {
  name: "repstats",
  components: {
    Bar,
  },
  data() {
    return {
      reportGenTime:null,
      orientationMode: null,
      voiceQuery: "",
      initialLoad: OrientationService.getInitialLoad(),
      disableList: {
        month: false,
      },
      chartFilterData: [],
      chartMode: OrientationService.getChartMode(),
      chartData: null,
      url: targetURL.LOCAL,
      error: false,
      errorMessage: null,
      ranges: {
        from: null,
        to: null,
      },
      todayDateFile: "RepStats_Report_" + new Date().toISOString() + ".xls",
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
      overalls: {
        sumbet: null,
        sumwin: null,
        regular:null,
        ctrbRegular:null,
        bonus:null,
        ctrbBonus:null,
        cashback:null,
        ctrbCashback:null,
        ggrRegular:null,
        ggrRegularMargin:null,
        ggr:null,
        ggrMargin:null
      },
      isMobile: false,
      page: 1,
      pageCount: 0,
      itemsPerPage: 32,
      isChannelDisabled: true,
      loadTable: false,
      monthDefault: 0,
      chartFilterDefault: 1,
      yearDefault: 2021,
      channelDefault: 1,
      slipTypeDefault: -1,
      aspectDefault: 3,
      channels: [
        {
          id: 0,
          title: "All",
        },
        {
          id: 1,
          title: "Online",
        },
        {
          id: 2,
          title: "Retail",
        },
      ],
      slipTypes: [
        {
          id: -1,
          title: "All",
        },
        {
          id: 0,
          title: "PreMatch",
        },
        {
          id: 1,
          title: "Live",
        },
        {
          id: 2,
          title: "Mixed",
        },
        {
          id: 3,
          title: "Outright",
        },
      ],
      aspects: [
        // {
        //   id: 0,
        //   title: "Ranges",
        // },
        // {
        //   id: 1,
        //   title: "Num of Evts",
        // },
        {
          id: 3,
          title: "Per day",
        },
        {
          id: 4,
          title: "Per year",
          disabled:true
        },
        {
          id: 5,
          title: "Per month",
          disabled:true
        }
        // },
        // {
        //   id: 2,
        //   title: "Providers",
        //   disabled: true,
        // },
      ],
      groupingByDateSegmentMonths: [
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
      months: [
        {
          id: 0,
          title: "All",
          from: "-01-01T08:00:00",
          to: "-01-01T08:00:00",
        },
        {
          id: 1,
          from: "-01-01T08:00:00",
          to: "-02-01T08:00:00",
          title: "January",
        },
        {
          from: "-02-01T08:00:00",
          to: "-03-01T08:00:00",
          id: 2,
          title: "February",
        },
        {
          from: "-03-01T08:00:00",
          to: "-04-01T08:00:00",
          id: 3,
          title: "March",
        },
        {
          from: "-04-01T08:00:00",
          to: "-05-01T08:00:00",
          id: 4,
          title: "April",
        },
        {
          from: "-05-01T08:00:00",
          to: "-06-01T08:00:00",
          id: 5,
          title: "May",
        },
        {
          from: "-06-01T08:00:00",
          to: "-07-01T08:00:00",
          id: 6,
          title: "June",
        },
        {
          from: "-07-01T08:00:00",
          to: "-08-01T08:00:00",
          id: 7,
          title: "July",
        },
        {
          from: "-08-01T08:00:00",
          to: "-09-01T08:00:00",
          id: 8,
          title: "August",
        },
        {
          from: "-09-01T08:00:00",
          to: "-10-01T08:00:00",
          id: 9,
          title: "September",
        },
        {
          from: "-10-01T08:00:00",
          to: "-11-01T08:00:00",
          id: 10,
          title: "October",
        },
        {
          from: "-11-01T08:00:00",
          to: "-12-01T08:00:00",
          id: 11,
          title: "November",
        },
        {
          from: "-12-01T08:00:00",
          to: "-01-01T08:00:00",
          id: 12,
          title: "December",
        },
      ],

      years: [
        {
          id: 0,
          title: "All",
          disabled: false,
        },
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
        {
          id: 2017,
          title:"2017"
        },
        {
          id: 2016,
          title:"2016"
        }
      ],
      search: "",
      tiketi: [],
      filters: {
        chart: 1,
        month: 0,
        year: 2021,
        channel: 1,
        slipType: -1,
        aspect: 3,
      },
    };
  },
  methods: {
    handleOrientationChange() {
      // create a SpeechRecognition object
      // const recognition = new window.webkitSpeechRecognition();

      // // configure setting that continuous results are returned for each recognition
      // recognition.continuous = true;

      // // configure setting that interim results should be returned
      // recognition.interimResults = true;

      // var that = this;
      // // event handler when a word or phrase has been positively recognized
      // recognition.onresult = function (event) {
      //   // console.log(event.results);
      //   for(let i=0; i<event.results.length;i++){
      //     for(let j=0; j<event.results[i].length; j++){

      //       console.log(event.results[i][j].transcript)
      //       var sortChart = document.getElementById("sortChart");

      //       if(event.results[i][j].transcript.includes("hide")){
      //         sortChart.style.display = "none";
      //       }

      //       if(event.results[i][j].transcript.includes("show")){
      //         sortChart.style.display = "block";
      //       }

      //       //RESET
      //       if(that.checkIf(event.results[i][j].transcript, "bet") && that.checkIfNotAlready(that.voiceQuery, "bet")){
      //         that.voiceQuery = event.results[i][j].transcript;
      //         that.chartFilterDefault = 1;
      //         that.filters.chart = 1;
      //         that.fillChartData(1);
      //       }

      //       //SUM
      //       if(that.checkIf(event.results[i][j].transcript, "sum") && that.checkIfNotAlready(that.voiceQuery, "sum")){
      //         that.voiceQuery = event.results[i][j].transcript;
      //         that.chartFilterDefault = 2;
      //         that.filters.chart = 2;
      //         that.fillChartData(2);
      //       }

      //       //AVERAGE
      //       if(that.checkIf(event.results[i][j].transcript, "avg") && that.checkIfNotAlready(that.voiceQuery, "avg")){
      //         that.voiceQuery = event.results[i][j].transcript;
      //         that.filters.chart = 3;
      //         that.chartFilterDefault = 3;
      //         that.fillChartData(3);
      //       }

      //       //ODDS
      //       if(that.checkIf(event.results[i][j].transcript, "odds") && that.checkIfNotAlready(that.voiceQuery, "odds")){
      //         that.voiceQuery = event.results[i][j].transcript;
      //         that.filters.chart = 4;
      //         that.chartFilterDefault = 4;
      //         that.fillChartData(4);
      //       }

      //       //EVENTS
      //       if(that.checkIf(event.results[i][j].transcript, "events") && that.checkIfNotAlready(that.voiceQuery, "events")){
      //         that.voiceQuery = event.results[i][j].transcript;
      //         that.filters.chart = 5;
      //         that.chartFilterDefault = 5;
      //         that.fillChartData(5);
      //       }

      //     }
      //   }
      // };
      // - SORTIRANJE GLASOM
      var that = this;
      var mql = window.matchMedia("(orientation: portrait)");
      mql.addListener(function (m) {
        if (m.matches) {
          // recognition.stop();
          that.orientationMode = "portrait";
          that.$nextTick(() => {
            that.chartMode = false;
            OrientationService.setChartMode(false);
          });
        } else {
          // recognition.start();
          that.orientationMode = "landscape";
          that.$nextTick(() => {
            that.chartMode = true;
            OrientationService.setChartMode(true);
          });
        }
      });
      // console.log(window.innerWidth)
      // console.log(window.innerHeight)
      // var orientation = window.innerWidth > window.innerHeight ? "landscape" : "portrait";
      // // const orientation = window.screen.orientation.type
    },
    checkIf(term, type) {
      if (type == "sum") {
        if (
          term.includes("sum") ||
          term.includes("some") ||
          term.includes("sound") ||
          term.includes("son")
        ) {
          return true;
        }
      }
      if (type == "bet") {
        if (term.includes("set")) {
          return true;
        }
      }
      if (type == "events") {
        if (term.includes("vents")) {
          return true;
        }
      }
      if (type == "avg") {
        if (
          term.includes("average") ||
          term.includes("rage") ||
          term.includes("avg")
        ) {
          return true;
        }
      }
      if (type == "odds") {
        if (
          term.includes("odds") ||
          term.includes("uote") ||
          term.includes("oots") ||
          term.includes("boots")
        ) {
          return true;
        }
      }
    },
    checkIfNotAlready(query, type) {
      if (type == "sum") {
        if (
          query.includes("sum") ||
          query.includes("some") ||
          query.includes("sound") ||
          query.includes("son")
        ) {
          return false;
        } else {
          return true;
        }
      }
      if (type == "bet") {
        if (query.includes("set")) {
          return false;
        } else {
          return true;
        }
      }
      if (type == "events") {
        return !query.includes("vents");
      }
      if (type == "avg") {
        if (
          query.includes("average") ||
          query.includes("rage") ||
          query.includes("avg")
        ) {
          return false;
        } else {
          return true;
        }
      }
      if (type == "odds") {
        if (
          query.includes("odds") ||
          query.includes("uote") ||
          query.includes("oots") ||
          query.includes("boots")
        ) {
          return false;
        } else {
          return true;
        }
      }
    },
    getLastDayOfMonth(month) {
      //0 - januar
      var d = new Date(new Date().getFullYear(), month + 1, 0);
      return d.getDate();
    },
    switchMode() {
      this.chartMode = !this.chartMode;
      OrientationService.setChartMode(!OrientationService.getChartMode());
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
    filterByChartColumn(criteria) {
      this.filters.chart = criteria;
      this.fillChartData(criteria);
    },
    filterByMonth(criteria) {
      this.filters.month = criteria;
    },
    filterByYear(criteria) {
      this.filters.year = criteria;
      if (criteria == 0 || this.filters.aspect == 4) {
        this.$nextTick(() => {
          this.filters.month = 0;
          this.monthDefault = 0;
        });
        this.disableList.month = true;
      } else {
        this.disableList.month = false;
      }
    },
    filterByChannel(criteria) {
      this.filters.channel = criteria;
    },
    filterBySlipType(criteria) {
      this.filters.slipType = criteria;
    },
    filterByAspect(criteria) {
      this.filters.aspect = criteria;
      if (criteria != 0) {
        this.errorMessage = "";
        this.ranges.from = null;
        this.ranges.to = null;
      }
      if (criteria == 4) {
          this.filters.month = 0;
          this.monthDefault = 0;
        this.disableList.month = true;
      } else {
        this.disableList.month = false;
      }
      if (criteria == 5) {
        this.years[0].disabled = true;
          this.filters.year = new Date().getFullYear();
          this.yearDefault = new Date().getFullYear();
      } else {
        this.years[0].disabled = false;
      }
    },
    //Formatting json
    formatJson(filterVal, jsonData) {
      return jsonData.map((v) => filterVal.map((j) => v[j]));
    },
    getData() {
      if (this.checkIfEligible()) {
        this.initialLoad = false;
        OrientationService.setInitialLoad(false);
        // let ADDITIONAL = 0;
        // if(this.filters.month==0 || this.filters.month==12)
        // ADDITIONAL = 1;

        this.chartMode = false;
        OrientationService.setChartMode(false);
        this.loadTable = true;
        this.tickets = [];
        this.emptyObject(this.overalls);
        let years = [];
        if (this.filters.year == 0) {
          for (let i = 2018; i <= new Date().getFullYear(); i++) {
            years.push(i.toString());
          }
        } else {
          years.push(this.filters.year.toString());
        }

        let monthFrom, monthTo;
        monthFrom =
          this.filters.year +
          this.groupingByDateSegmentMonths.filter(
            (x) => x.id == this.filters.month
          )[0].from;
        monthTo =
          this.filters.year +
          this.groupingByDateSegmentMonths.filter(
            (x) => x.id == this.filters.month
          )[0].to;
        if (this.filters.year == 0) {
          monthFrom = "2018-01-01";
          monthTo = new Date().getFullYear() + "-12-31";
        }
        this.reportGenTime = null;
        axios
          .post(this.url + "/api/RepStats", {
            rangeFrom: this.ranges.from,
            rangeTo: this.ranges.to,
            year: years,
            monthFrom,
            monthTo,
            channel: this.filters.channel,
            slipType: this.filters.slipType,
            aspect: this.filters.aspect,
          })
          .then((response) => {
            if (!response.tiket) {
              this.chartData = null;
            }
            var d = new Date();
            this.reportGenTime = d.getHours()+"h "+d.getMinutes()+"m "+d.getSeconds()+"s";
            this.formatTicket(response);
            this.loadTable = false;
          });
      }
    },
    isNegative(val) {
      return val == null || val == "";
    },
    checkIfEligible() {
      if (this.filters.aspect != 0) {
        this.error = false;
        this.errorMessage = null;
        return true;
      }
      if (
        parseInt(this.ranges.from) >= parseInt(this.ranges.to) ||
        parseInt(this.ranges.from) < 20
      ) {
        this.errorMessage = "Values in range fields are not valid";
        this.error = true;
        return false;
      }
      if (
        this.isNegative(this.ranges.from) &&
        this.isNegative(this.ranges.to)
      ) {
        this.errorMessage = null;
        this.error = false;
        return true;
      }
      if (
        !this.isNegative(this.ranges.from) ||
        !this.isNegative(this.ranges.to)
      ) {
        if (
          !this.isNegative(this.ranges.from) &&
          this.isNegative(this.ranges.to)
        ) {
          this.errorMessage =
            "In order to perform custom range search you need to fill out both fields";
          this.error = true;
          return false;
        }
        if (
          this.isNegative(this.ranges.from) &&
          !this.isNegative(this.ranges.to)
        ) {
          this.errorMessage =
            "In order to perform custom range search you need to fill out both fields";
          this.error = true;
          return false;
        }
        this.errorMessage = null;
        this.error = false;
        return true;
      }
    },
    emptyObject(obj) {
      for (const [key] of Object.entries(obj)) {
        obj[key] = null;
      }
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
      if (Object.keys(response.data.tiket).length > 0) {
        // && response.data.tiket.filter((x) => x.Opseg == "van opsega").length>1

        if (
          Object.keys(response.data.tiket).length == 1 &&
          response.data.tiket.filter((x) => x.Opseg == "van opsega").length == 1
        ) {
          this.tickets = [];
        } else {
          this.tickets = response.data.tiket.filter(
            (x) => x.Opseg != "van opsega"
          );
          // this.tickets.pop()
          this.tickets.forEach((ticket) => {
            ticket["Bet"] = this.convertToReadableNumber(ticket["Bet"]);
            ticket["SumBet"] = this.convertToCurrency(ticket["SumBet"]);
            ticket["SumWin"] = this.convertToCurrency(ticket["SumWin"]);
            ticket["SumRegularWin"] = this.convertToCurrency(ticket["SumRegularWin"]);
            ticket["CtrbRegular"] = (ticket["CtrbRegular"]*100).toFixed(2)+"%";
            ticket["SumBonusWin"] = this.convertToCurrency(ticket["SumBonusWin"]);
            ticket["CtrbBonus"] = (ticket["CtrbBonus"]*100).toFixed(2)+"%";
            ticket["SumCashbackWin"] = this.convertToCurrency(ticket["SumCashbackWin"]);
            ticket["CtrbCashback"] = (ticket["CtrbCashback"]*100).toFixed(2)+"%";
            ticket["GgrRegular"] = this.convertToCurrency(ticket["GgrRegular"]);
            ticket["GgrRegularMargin"] = (ticket["GgrRegularMargin"]*100).toFixed(2)+"%";
            ticket["Ggr"] = this.convertToCurrency(ticket["Ggr"]);
            ticket["GgrMargin"] = (ticket["GgrMargin"]*100).toFixed(2)+"%";
          });
          this.createOveralls();
          this.mapStakes();
        }
      } else {
        this.tickets = [];
      }
      this.json_data = this.tickets;
      console.log(this.json_data)
    },
    convertToCleanFloat(num) {
      return num.replace("$", "").replace(/,/g, "");
    },
    createOveralls() {
      //c - stands for cumulative
      let cSumWin = this.tickets.reduce(
        (a, b) => a + this.fromCurrencyToFloat(b["SumWin"]),
        0
      );
      let cSumBet = this.tickets.reduce(
        (a, b) => a + this.fromCurrencyToFloat(b["SumBet"]),
        0
      );
      let cSumRegularWin = this.tickets.reduce(
        (a, b) => a + this.fromCurrencyToFloat(b["SumRegularWin"]),
        0
      );
      let cSumBonusWin = this.tickets.reduce(
        (a, b) => a + this.fromCurrencyToFloat(b["SumBonusWin"]),
        0
      );
      let cSumCashbackWin = this.tickets.reduce(
        (a, b) => a + this.fromCurrencyToFloat(b["SumCashbackWin"]),
        0
      );
      this.overalls.sumwin = this.convertToCurrency(cSumWin);
      this.overalls.sumbet = this.convertToCurrency(cSumBet);
      this.overalls.regular = this.convertToCurrency(cSumRegularWin)
      this.overalls.ctrbRegular = (this.convertToCurrency(
          this.fromCurrencyToFloat(this.overalls.regular) /
          this.fromCurrencyToFloat(this.overalls.sumwin)
      )*100).toFixed(2)+"%";
      this.overalls.bonus = this.convertToCurrency(cSumBonusWin)
      this.overalls.ctrbBonus = ((
          this.fromCurrencyToFloat(this.overalls.bonus) /
          this.fromCurrencyToFloat(this.overalls.sumwin)
      )*100).toFixed(2)+"%";
      this.overalls.cashback = this.convertToCurrency(cSumCashbackWin)
      this.overalls.ctrbCashback = ((
          this.fromCurrencyToFloat(this.overalls.cashback) /
          this.fromCurrencyToFloat(this.overalls.sumwin)
      )*100).toFixed(2)+"%";
      this.overalls.ggrRegular = this.convertToCurrency(
          this.fromCurrencyToFloat(this.overalls.sumbet) -
          this.fromCurrencyToFloat(this.overalls.regular)
      )
      this.overalls.ggrRegularMargin = ((
          this.fromCurrencyToFloat(this.overalls.ggrRegular) /
          this.fromCurrencyToFloat(this.overalls.sumbet)
      )*100).toFixed(2)+"%";
      this.overalls.ggr = this.convertToCurrency(
          this.fromCurrencyToFloat(this.overalls.sumbet) -
          this.fromCurrencyToFloat(this.overalls.sumwin)
      )
      this.overalls.ggrMargin = ((
          this.fromCurrencyToFloat(this.overalls.ggr) /
          this.fromCurrencyToFloat(this.overalls.sumbet)
      )*100).toFixed(2)+"%";
    },
    mapStakes() {
      this.tickets.sort((a, b) => (a.Opseg > b.Opseg ? 1 : -1));
      var months = [
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
      if (!this.isDayFiltering()) {
        this.tickets.forEach((ticket) => {
          if (this.filters.aspect == 5) {
            ticket["Opseg"] = months[ticket["Opseg"] - 1];
          } else {
            switch (ticket["Opseg"]) {
              case "custom":
                ticket["Opseg"] =
                  "(" + this.ranges.from + ", " + this.ranges.to + "]";
                break;
              case "a":
                ticket["Opseg"] = "[20, 100]";
                break;
              case "b":
                ticket["Opseg"] = "(50, 100]";
                break;
              case "c":
                ticket["Opseg"] = "(100, 500]";
                break;
              case "d":
                ticket["Opseg"] = "(500, 1000]";
                break;
              case "e":
                ticket["Opseg"] = "(1000, 2000]";
                break;
              case "f":
                ticket["Opseg"] = "(2000, 5000]";
                break;
              case "g":
                ticket["Opseg"] = "(5000, 10 000]";
                break;
              case "h":
                ticket["Opseg"] = "(10 000, 20 000]";
                break;
              case "i":
                ticket["Opseg"] = "(20 000, 50 000]";
                break;
              case "j":
                ticket["Opseg"] = "(50 000, 100 000]";
                break;
              case "k":
                ticket["Opseg"] = "(100 000, 200 000]";
                break;
              case "l":
                ticket["Opseg"] = "(200 000, 500 000]";
                break;
              case "m":
                ticket["Opseg"] = "(500 000, 15 000 000]";
                break;
              case "n":
                ticket["Opseg"] = "(0, 1]";
                break;
              case "o":
                ticket["Opseg"] = "(1, 2]";
                break;
              case "p":
                ticket["Opseg"] = "(2, 3]";
                break;
              case "q":
                ticket["Opseg"] = "(3, 4]";
                break;
              case "r":
                ticket["Opseg"] = "(4, 5]";
                break;
              case "s":
                ticket["Opseg"] = "(5, 6]";
                break;
              case "t":
                ticket["Opseg"] = "(6, 7]";
                break;
              case "u":
                ticket["Opseg"] = "(7, 9]";
                break;
              case "v":
                ticket["Opseg"] = "(9, 12]";
                break;
              case "w":
                ticket["Opseg"] = "(12, 16]";
                break;
              case "x":
                ticket["Opseg"] = "(16, 20]";
                break;
              case "y":
                ticket["Opseg"] = "(20, 40]";
                break;
              default:
                break;
            }
          }
        });
      } else {
        this.tickets.forEach((tiket) => {
          let datePrep = new Date(tiket["Opseg"]);
          if (this.filters.year == 0) {
            tiket["Opseg"] =
              datePrep.getDate() +
              ". " +
              months[datePrep.getMonth()] +
              " " +
              datePrep.getFullYear() +
              ".";
          } else {
            tiket["Opseg"] =
              datePrep.getDate() + ". " + months[datePrep.getMonth()];
          }
        });
      }
      this.fillChartData();
    },
    random_rgba() {
      var o = Math.round,
        r = Math.random,
        s = 255;
      return (
        "rgba(" +
        o(r() * s) +
        "," +
        o(r() * s) +
        "," +
        o(r() * s) +
        "," +
        1 +
        ")"
      );
    },
    fillChartData(criteria = 1) {
      //filter data
      Object.keys(this.tickets[0]).forEach((value, key) => {
        if (value != "Opseg" && value != "margin" && !value.includes("ctrb")) {
          this.chartFilterData.push({
            id: key,
            title: this.customMapTableHeader(value),
          });
        }
      });
      //labels
      let labels = this.tickets.map((x) => x.Opseg);
      let legendName = "";
      let backgroundColor, data;
      let IS_PER_YEAR = this.filters.aspect == 4;
      switch (criteria) {
        case 1:
          backgroundColor = [];
          for (let i = 0; i < labels.length; i++) {
            backgroundColor.push(IS_PER_YEAR ? this.random_rgba() : "blue");
          }
          data = this.tickets.map((x) => x.Bet.replace(/,/g, ""));
          legendName = "Broj betova";
          break;
        case 2:
          backgroundColor = [];
          for (let i = 0; i < labels.length; i++) {
            backgroundColor.push(IS_PER_YEAR ? this.random_rgba() : "red");
          }
          data = this.tickets.map((x) => x.SumBet.replace(/,/g, ""));
          legendName = "Suma betova";
          break;
        case 3:
          backgroundColor = [];
          for (let i = 0; i < labels.length; i++) {
            backgroundColor.push(
              IS_PER_YEAR ? this.random_rgba() : "indianred"
            );
          }
          data = this.tickets.map((x) => x.AvgBet.replace(/,/g, ""));
          legendName = "Prosek betova";
          break;
        case 4:
          backgroundColor = [];
          for (let i = 0; i < labels.length; i++) {
            backgroundColor.push(IS_PER_YEAR ? this.random_rgba() : "green");
          }
          data = this.tickets.map((x) => x.GwaOdds.replace(/,/g, ""));
          legendName = "GWA Odds";
          break;
        case 5:
          backgroundColor = [];
          for (let i = 0; i < labels.length; i++) {
            backgroundColor.push(IS_PER_YEAR ? this.random_rgba() : "orange");
          }
          data = this.tickets.map((x) => x.GwaEvents.replace(/,/g, ""));
          legendName = "GWA Events";
          break;
        case 6:
          backgroundColor = [];
          for (let i = 0; i < labels.length; i++) {
            backgroundColor.push(IS_PER_YEAR ? this.random_rgba() : "pink");
          }
          data = this.tickets.map((x) => x.Win.replace(/,/g, ""));
          legendName = "Broj winova";
          break;
        case 7:
          backgroundColor = [];
          for (let i = 0; i < labels.length; i++) {
            backgroundColor.push(IS_PER_YEAR ? this.random_rgba() : "yellow");
          }
          data = this.tickets.map((x) => x.CtrbBets.replace(/,/g, ""));
          legendName = "Contribution Bets";
          break;
        case 8:
          backgroundColor = [];
          for (let i = 0; i < labels.length; i++) {
            backgroundColor.push(
              IS_PER_YEAR ? this.random_rgba() : "oceanblue"
            );
          }
          data = this.tickets.map((x) => x.SumWin.replace(/,/g, ""));
          legendName = "Suma winova";
          break;
        case 9:
          backgroundColor = [];
          for (let i = 0; i < labels.length; i++) {
            backgroundColor.push(IS_PER_YEAR ? this.random_rgba() : "brown");
          }
          data = this.tickets.map((x) => x.ggr.replace(/,/g, ""));
          legendName = "Suma GGR";
          break;
        case 10:
          backgroundColor = [];
          for (let i = 0; i < labels.length; i++) {
            backgroundColor.push(
              IS_PER_YEAR ? this.random_rgba() : "olivegreen"
            );
          }
          data = this.tickets.map((x) => x.margin.replace(/,/g, ""));
          legendName = "Suma Margin";
          break;
        default:
          break;
      }

      let obj = {
        labels: labels,
        datasets: [
          {
            label: legendName + " po opsezima",
            borderWidth: 1,
            backgroundColor: backgroundColor,
            pointBorderColor: "#2554FF",
            data: data,
          },
        ],
      };
      this.chartData = obj;
      if (OrientationService.getChartMode()) this.forceRender();
    },
    forceRender() {
      this.chartMode = false;
      OrientationService.setChartMode(false);
      this.$nextTick(() => {
        this.chartMode = true;
        OrientationService.setChartMode(true);
      });
    },
    isDayFiltering() {
      return (
        this.tickets.filter((x) => x.Opseg.toString().includes("-")).length > 0
      );
    },
    customMapTableHeader(value) {
      switch (value) {
        case "SumBet":
          return "ΣBET";
        case "SumWin":
          return "ΣWIN";
        case "SumRegularWin":
          return "Regular";
        case "SumBonusWin":
          return "Bonus";
        case "SumCashbackWin":
          return "Cashback";
        case "ΣGGR (REGULAR)":
          return "GgrRegular";
        case "ΣGGR":
          return "Ggr";
        default:
          return "Unknown column";
      }
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
          text: "Period",
          align: "start",
          value: "Opseg",
        },
        {
          text: "ΣBet",
          value: "SumBet",
        },
        {
          text: "ΣWin",
          value: "SumWin",
        },
        {
          text: "Regular",
          value: "SumRegularWin",
        },
        {
          text: "Ctrb",
          value: "CtrbRegular",
        },
        {
          text: "Bonus",
          value: "SumBonusWin",
        },
        {
          text: "Ctrb",
          value: "CtrbBonus",
        },
        {
          text: "Cashback",
          value: "SumCashbackWin",
        },
        {
          text: "Ctrb",
          value: "CtrbCashback",
        },
        {
          text: "ΣGGR (regular)",
          value: "GgrRegular",
        },
        {
          text: "Margin",
          value: "GgrRegularMargin",
        },
        {
          text: "ΣGGR",
          value: "Ggr",
        },
        {
          text: "Margin",
          value: "GgrMargin",
        }
      ];
    },
  },
  created() {
    // window.addEventListener(
    //   "orientationchange",
    //   this.handleOrientationChange
    // );
    this.initialLoad = true;
    this.handleOrientationChange();
    this.determineURL();
    this.tickets = [];
    // axios
    //   .get(this.url + "/api/Tiket")
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
.mobile {
  color: #333;
}
.v-toolbar__content {
  background-color: #225e0d !important;
}
@media screen and (min-width: 768px) {
  #report4 table {
    border-top: 1px solid black;
  }
  #report4 .mainHeader:nth-child(7),
  #report4 .mainHeader:nth-child(9) {
    border-right: 1px solid black;
  }
  #report4 .mainHeader:first-child{
        background: lightblue;
        border:none!important
  }
  #report4 .mainHeader:nth-child(2) {
    border-left: 1px solid black;
    border-right: 1px solid black;
    background: lightblue;
  }
 #report4 .mainHeader:nth-child(3){
   background:red;
   color:white
 }
 #report4 .mainHeader:nth-child(3),
 #report4 .mainHeader:nth-child(5)
{
    border-right: 1px solid black;
}

 #report4 .mainHeader:nth-child(4),
 #report4 .mainHeader:nth-child(5),
 #report4 .mainHeader:nth-child(6),
 #report4 .mainHeader:nth-child(7),
 #report4 .mainHeader:nth-child(8),
 #report4 .mainHeader:nth-child(9){
   background:darksalmon;
 }

 #report4 .mainHeader:nth-child(10),
 #report4 .mainHeader:nth-child(11),
 #report4 .mainHeader:nth-child(12),
 #report4 .mainHeader:nth-child(13){
   background: yellowgreen;
 }

#report4 .mainHeader{
  border-top: 1px solid black;
  text-align: left!important;
}

  #report4 table td + td:nth-child(2),
  #report4 table td + td:nth-child(4),
  #report4 table td + td:nth-child(10) {
    border-left: 1px solid black;
  }
  #report4 table td + td:nth-child(2),
  #report4 table td + td:nth-child(7),
  #report4 table td + td:nth-child(5){
    border-right: 1px solid black;
  }
}
.chartsMode {
  display: block;
}
@media screen and (max-width: 768px) {
  .chartsMode {
    display: none;
  }
  .desktop,
  .v-data-table-header tr {
    height: 55px !important;
  }
  .mobile table tr {
    max-width: 100%;
    position: relative;
    display: block;
    height: 250px;
  }

  .mobile table tr:nth-child(odd) {
    border-left: 6px solid rgb(48, 170, 103);
  }

  .mobile table tr:nth-child(even) {
    border-left: 6px solid rgb(174, 179, 179);
  }

  .mobile table tr td {
    display: flex;
    width: 100%;
    /* border-bottom: 1px solid #f5f5f5; */
    height: auto;
    padding: 10px;
  }

  .mobile table tr td ul li:before {
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
  .mobile .theme--light tbody tr:hover:not(.v-datatable__expand-row) {
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

.home {
  width: 100%;
}

.container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

.quote {
  width: 29%;
  padding: 0.5rem;
  margin: 1%;
  border-radius: 10px;
  border: 1px solid steelblue;
  color: black;
}

.quote span.by {
  text-decoration: underline;
}

.quote .added-by {
  color: rgba(0, 0, 0, 0.6);
  margin-top: 3em;
}
@media screen and (orientation: landscape) {
  #bar-chart {
    height: 200px !important;
    width: 80% !important;
    margin: 0 auto !important;
  }
}
</style>
