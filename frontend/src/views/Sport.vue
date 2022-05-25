<template>
  <div>
    <v-container fluid>
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
      <v-row align="center" style="display:none">
        <v-col class="d-flex" cols="12" sm="6">
          <v-select
            :items="channels"
            item-value="id"
            item-text="title"
            :disabled="true"
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
      </v-row>
            <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-autocomplete
            :items="sports"
            item-value="id"
            item-text="title"
            v-model="sportDefault"
            label="Select Sport"
            v-on:change="filterBySport"
          ></v-autocomplete>
        </v-col>
      </v-row>
            <v-row align="center">
        <v-col class="d-flex" cols="12" sm="6">
          <v-autocomplete
            :items="competitions"
            item-value="id"
            item-text="title"
            v-model="competitionDefault"
            label="Select Competition"
            v-on:change="filterByCompetition"
          ></v-autocomplete>
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
              style="
                margin-top: -8px;
                margin-left: 3px;
                width: 40px;
                cursor: pointer;
              "
            />
          </export-excel>
          <img 
            v-if="!chartMode && chartData && !initialLoad && tiketi.length>0"
            src="@/assets/charts2.png"
            style="
                height:35px;
                margin-top:2px;
                cursor: pointer;
              "
            @click="switchMode"
          />
          <img 
            v-if="chartMode && !initialLoad"
            src="@/assets/table.png"
            style="
                height:40px;
                margin-top:-2px;
                cursor: pointer;
              "
            @click="switchMode"
          />
        </v-col>
      </v-row>
    </v-container>
    <v-layout v-if="!initialLoad  && !advancedLoaded" v-resize="onResize" column style="padding-top: 56px">
      <v-data-table
        v-if="!chartMode"
        id="report1"
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
          <tr style="text-align:center">
            <th></th>
            <th
              colspan="5"
              style="
                border-left: 1px solid black;
                border-right: 1px solid black;
              "
            >
              Turnover
            </th>
            <th colspan="3" style="border-right: 1px solid black">Winnings</th>
            <th colspan="2">GGR Margin</th>
          </tr>
          <tr>
            <th
              class="mainHeader"
              style="text-align: left; padding-left: 15px; padding-top: 10px"
              v-for="head in props.headers"
              :key="head.text"
            >
              {{ head.text.toUpperCase() }}
            </th>
          </tr>
          <tr>
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
              {{ overalls.bet }}
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
              {{ overalls.avgBetSum }}
            </th>
            <th
              colspan="2"
              style="
                text-align: left;
                padding-left: 15px;
                border-right: 1px solid black;
                padding-bottom: 5px;
                padding-top: 5px;
                border-top: 1px solid black;
                border-bottom: 1px solid black;
              "
            ></th>
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
              {{ overalls.win }}
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
            >{{overalls.ctrbSum}}</th>
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
              {{ overalls.sumggr }}
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
              {{ overalls.marginudeo }}
            </th>
          </tr>
        </template>
        <template v-slot:item="{ item }">
          <tr v-if="!isMobile">
            <td>{{ item.Date }}</td>
            <td class="text-xs-right">{{ item.Bet }}</td>
            <td class="text-xs-right">{{ item.SumBet }}</td>
            <td class="text-xs-right">{{ item.AvgBet }}</td>
            <td class="text-xs-right">{{ item.GwaOdds }}</td>
            <td class="text-xs-right">{{ item.GwaEvents }}</td>
            <td class="text-xs-right">{{ item.Win }}</td>
            <td class="text-xs-right">{{ item.CtrbBets }}</td>
            <td class="text-xs-right">{{ item.SumWin }}</td>
            <td class="text-xs-right">{{ item.ggr }}</td>
            <td class="text-xs-right">{{ item.margin }}</td>
          </tr>
          <tr id="mobileRow" v-else>
            <td
              style="
                border-top: thin solid rgba(0, 0, 0, 0.12);
                border-bottom: none;
              "
            >
              <ul class="flex-content">
                <li class="flex-item" data-label="STAKE">
                  {{ item.Date }}
                </li>
                <li class="flex-item" data-label="#BET">
                  {{ item.Bet }}
                </li>
                <li class="flex-item" data-label="ΣBET">
                  {{ item.SumBet }}
                </li>
                <li class="flex-item" data-label="AVG.BET">
                  {{ item.AvgBet }}
                </li>
                <li class="flex-item" data-label="GWA.ODDS">
                  {{ item.GwaOdds }}
                </li>
                <li class="flex-item" data-label="GWA.EVENTS">
                  {{ item.GwaEvents }}
                </li>
                <li class="flex-item" data-label="#WIN">
                  {{ item.Win }}
                </li>
                <li class="flex-item" data-label="CTRB.#BETS">
                  {{ item.CtrbBets }}
                </li>
                <li class="flex-item" data-label="ΣWIN">
                  {{ item.SumWin }}
                </li>
                <li class="flex-item" data-label="ΣGGR">
                  {{ item.ggr }}
                </li>
                <li class="flex-item" data-label="MARGIN">
                  {{ item.margin }}
                </li>
              </ul>
            </td>
          </tr>
        </template>
      </v-data-table>
      <template v-if="chartMode">
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
      </template>
    </v-layout>
    <v-layout v-if="!initialLoad  && advancedLoaded" v-resize="onResize" column style="padding-top: 56px">
      <v-data-table
        v-if="!chartMode"
        id="report3"
        :headers="headers2"
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
            <th
              style="text-align: left; padding-left: 15px; padding-top: 10px"
              v-for="head in props.headers"
              :key="head.text"
            >
              {{ head.text.toUpperCase() }}
            </th>
          </tr>
        </template>
        <template v-slot:item="{ item }">
          <tr v-if="!isMobile">
            <td>{{ item.Date }}</td>
            <td class="text-xs-right">{{ item.HomeCompetitorName }}</td>
            <td class="text-xs-right">{{ item.AwayCompetitorName }}</td>
            <td class="text-xs-right">{{ item.HomeValue }}</td>
            <td class="text-xs-right">{{ item.AwayValue }}</td>
            <td class="text-xs-right">{{ item.numberOfBets }}</td>
            <td class="text-xs-right">{{ item.SumBet }}</td>
            <td class="text-xs-right">{{ item.SumWin }}</td>
            <td class="text-xs-right">{{ item.ggr }}</td>
            <td class="text xs-right">
              <div class="text-center">
                <v-btn
          color="red lighten-2"
          dark
          @click.prevent="open(item)"
        >
          Details
        </v-btn>
  </div>
            </td>
          </tr>
          <tr id="mobileRow" v-else>
            <td
              style="
                border-top: thin solid rgba(0, 0, 0, 0.12);
                border-bottom: none;
              "
            >
              <ul class="flex-content">
                <li class="flex-item" data-label="DATE">
                  {{ item.Date }}
                </li>
                <li class="flex-item" data-label="HOME">
                  {{ item.HomeCompetitorName }}
                </li>
                <li class="flex-item" data-label="AWAY">
                  {{ item.AwayCompetitorName }}
                </li>
                <li class="flex-item" data-label="HOME SCORE">
                  {{ item.HomeValue }}
                </li>
                <li class="flex-item" data-label="AWAY SCORE">
                  {{ item.AwayValue }}
                </li>
                <li class="flex-item" data-label="ΣBET">
                  {{ item.numberOfBets }}
                </li>                
                <li class="flex-item" data-label="ΣBET">
                  {{ item.SumBet }}
                </li>
                <li class="flex-item" data-label="ΣWIN">
                  {{ item.SumWin }}
                </li>
                <li class="flex-item" data-label="ΣGGR">
                  {{ item.ggr }}
                </li>
                <li>
                        <div class="text-center">
                <v-btn
          color="red lighten-2"
          style="margin-top:25px"
          dark
          @click.prevent="open(item)"
        >
          Details
        </v-btn>
  </div>
                </li>
              </ul>c
            </td>
          </tr>
        </template>
      </v-data-table>
      <v-dialog
      v-model="dialog"
      content-class="super"
    >

      <v-card>
        <v-card-title class="headline grey lighten-2" v-bind:style="{fontSize:isMobile?'14px!important':'auto'}">
          {{selectedLine.Date}} - ({{selectedLine.HomeCompetitorName}} - {{selectedLine.AwayCompetitorName}}) ({{selectedLine.HomeValue}} : {{selectedLine.AwayValue}})
        </v-card-title>

        <v-card-text>
          <table :class="{f9:isMobile}">
            <thead>
              <tr>
                <th colspan="3">Igra</th>
                <th>ΣBET</th>
                <th v-if="!isMobile">ΣWIN</th>
                <th>ΣGGR</th>
              </tr>
              <tr v-for="match in dialogData" :key="match.unique">
                <td colspan="3">{{match.BetGameName}} | {{match.BetGameOutcomeName}} | {{match.Granica}}</td>
                <td>{{convertToCurrency(match.SumBet)}}</td>
                <td v-if="!isMobile">{{convertToCurrency(match.SumWin)}}</td>
                <td>{{convertToCurrency(match.SumBet-match.SumWin)}}</td>
              </tr>
            </thead>
          </table>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="dialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
      <template v-if="chartMode">
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
      </template>
    </v-layout>
    <div class="text-center pt-2">
      <v-pagination
        v-if="tickets.length > 32 && !chartMode"
        v-model="page"
        :length="pageCount"
      ></v-pagination>
    </div>
  </div>
</template>

<script>
var _ = require('lodash');
const axios = require("axios").default;
import { targetURL } from "../global/config";
import Bar from "../views/charts/Bar.vue";
export default {
  name: "sport",
  components: {
    Bar,
  },
  data() {
    return {
      dialogData:[],
      groupedMatches:[],
      dialog:false,
      advancedLoaded:false,
      sports:[],
      competitions:[],
      initialLoad: true,
      disableList:{
        month:false
      },
      chartFilterData: [],
      chartMode: false,
      chartData: null,
      url: targetURL.LOCAL,
      error: false,
      errorMessage: null,
      todayDateFile: "Sport_Report_"+new Date().toISOString() + ".xls",
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
        win: null,
        sumwin: null,
        bet: null,
        sumbet: null,
        sumggr: null,
        marginudeo: null,
        ctrbSum:null,
        avgBetSum:null
      },
      isMobile: false,
      page: 1,
      pageCount: 0,
      itemsPerPage: 32,
      isChannelDisabled: true,
      loadTable: true,
      monthDefault: 0,
      chartFilterDefault: 1,
      yearDefault: 2021,
      channelDefault: 1,
      slipTypeDefault: null,
      aspectDefault: 1,
      sportDefault:1,
      competitionDefault:0,
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
          id: null,
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
        {
          id: 1,
          title: "Per day",
        },
        {
          id: 2,
          title : "Per month"   
        },
        {
          id: 3,
          title: "Per year"
        },
        {
          id:4,
          title:"Advanced Per Day"
        }
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
      selectedLine:{},
      filters: {
        sport:1,
        competition:0,
        month: 0,
        year: 2021,
        channel: 1,
        slipType: null,
        aspect: 1,
      },
    };
  },
  methods: {
    open(item){
      this.dialog=true;
      this.selectedLine.MatchId = item.MatchId;
      this.selectedLine.Date=  item.Date;
      this.selectedLine.HomeCompetitorName = item.HomeCompetitorName;
      this.selectedLine.AwayCompetitorName = item.AwayCompetitorName;
      this.selectedLine.HomeValue = item.HomeValue;
      this.selectedLine.AwayValue = item.AwayValue;
      this.dialogData = this.getInfo(item.MatchId)
    },
    getInfo(id){
      var arr = [];
      var numberOfBets = this.groupedMatches.filter(x=>x.MatchId=id).length;
      this.groupedMatches.filter(x=>x.MatchId==id).forEach(d=>{
        
        if( !arr[parseInt(d.BetGameId+''+d.BetGameOutcomeId)] ){  
            arr[parseInt(d.BetGameId+''+d.BetGameOutcomeId)] = []; 
        } 
        arr[parseInt(d.BetGameId+''+d.BetGameOutcomeId)].push(d); 

      }
      )
      var finalData=[]
      var obj = {}
      var sumBet = 0;
      var sumWin = 0;
      var passedFirst = false;
      arr.forEach(el=>{
      el.forEach(el2=>{
        if(!passedFirst){
          obj.numberOfBets = numberOfBets;
          sumBet+=el2.SumBet
          sumWin+=el2.SumWin
          obj.Date = el2.Date;
          obj.HomeCompetitorName = el2.HomeCompetitorName
          obj.AwayCompetitorName = el2.AwayCompetitorName
          obj.HomeValue = el2.HomeValue
          obj.AwayValue = el2.AwayValue
          obj.BetGameName = el2.BetGameName
          obj.BetGameOutcomeName = el2.BetGameOutcomeName
          obj.MatchId = el2.MatchId
          obj.Granica = el2.Granica
          obj.SlipId = el2.SlipId
          passedFirst=true;
        } else {
          sumBet+=el2.SumBet
          sumWin+=el2.SumWin
        }
      })
      obj.SumBet = sumBet;
      obj.SumWin = sumWin;
      obj.ggr = sumBet-sumWin;
      finalData.push(_.cloneDeep(obj));
      sumBet = 0;
      sumWin = 0;
      passedFirst = false;
    })
    let ordered = _.orderBy(finalData, ['ggr'], ['asc']);
  
      return ordered
    },
    getLastDayOfMonth(month){
      //0 - januar
      var d = new Date(new Date().getFullYear(), month + 1, 0);
      return d.getDate()
    },
    switchMode() {
      this.chartMode = !this.chartMode;
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
    filterBySport(criteria) {
      this.filters.sport = criteria;
      this.sports = this.allSports;
      this.competitions = this.allCompetitions;
      let cs = _.cloneDeep(this.competitions.filter(x=>x.cs_id==criteria))
      this.competitions = cs;
      this.filters.competition = this.competitions[0].id
      this.competitionDefault = this.filters.competition        
      this.competitions.unshift({id:null, title:'All Competitions'})
      
    },
    filterByCompetition(criteria) {
      this.filters.competition = criteria;
    },
    filterByYear(criteria) {
      this.filters.year = criteria;
      if(this.filters.aspect==3){
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
      if(criteria!=0 && this.filters.aspect==4){
        this.aspectDefault = 1;
        this.filters.aspect = 1;
      }
    },
    filterByAspect(criteria) {
      this.filters.aspect = criteria;
      if(criteria == 3){
       this.$nextTick(() => {
        this.filters.month = 0;
        this.monthDefault = 0;
        });
        this.disableList.month = true;
      } else if(criteria==2) {
        this.$nextTick(() => {
        this.filters.month = new Date().getMonth()+1;
        this.monthDefault = new Date().getMonth()+1;
        this.filters.year = new Date().getFullYear();
        this.yearDefault = new Date().getFullYear();
        });
      } else {
        this.disableList.month = false;
        this.months[0].disabled = false;
      }

      if(criteria == 4){
        this.slipTypeDefault = 0;
        this.filters.slipType = 0;
      }
    },
    //Formatting json
    formatJson(filterVal, jsonData) {
      return jsonData.map((v) => filterVal.map((j) => v[j]));
    },
    getData() {
        this.advancedLoaded = this.filters.aspect==4;
        this.initialLoad = false;

        this.chartMode = false;
        this.loadTable = true;
        this.tickets = [];
        this.emptyObject(this.overalls);
        let yearFrom = this.years.filter((x) => x.id == this.filters.year)[0].id;
        let yearTo = this.years.filter((x) => x.id == this.filters.year)[0].id;
        if(this.filters.year == 0){
          yearFrom = 2018;
          yearTo = new Date().getFullYear();
        }
        let month = this.months.filter((x) => x.id == this.filters.month)[0].id;
        let monthFrom, monthTo;
        if([1,2,3,4].includes(this.filters.aspect)){
        monthFrom = yearFrom+this.groupingByDateSegmentMonths.filter(x=>x.id==this.filters.month)[0].from
        monthTo = yearTo+this.groupingByDateSegmentMonths.filter(x=>x.id==this.filters.month)[0].to
        } else {
        monthFrom = yearFrom +
              this.months.filter((x) => x.id == this.filters.month)[0].from;
        monthTo =  month == 12 || month == 0
                ? yearTo +
                  1 +
                  this.months.filter((x) => x.id == this.filters.month)[0].to
                : yearTo +
                  this.months.filter((x) => x.id == this.filters.month)[0].to;
        }


        axios
          .post(this.url + "/api/SportReport", {
            year: this.filters.year,
            sportId:this.filters.sport,
            competitionId:this.filters.competition, 
            monthFrom,
            monthTo,
            channel: this.filters.channel,
            slipType: this.filters.slipType,
            aspect: this.filters.aspect,
          })
          .then((response) => {
            if(!response.tiket){
              this.chartData = null;
            }
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
    fromCurrencyToFloat(value) {
      value = value+''
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
        if(this.advancedLoaded){
          this.prepareAdvanced(response.data.tiket)
        } else {
          this.tickets = response.data.tiket.filter(
          (x) => x.Date != "van opsega"
        );

        this.tickets.forEach((ticket) => {
          ticket["Bet"] = this.convertToReadableNumber(ticket["Bet"]);
          ticket["SumBet"] = this.convertToCurrency(ticket["SumBet"]);
          ticket["AvgBet"] = this.convertToCurrency(ticket["AvgBet"]);
          ticket["GwaOdds"] = this.convertToCurrency(ticket["GwaOdds"]);
          ticket["GwaEvents"] = this.convertToCurrency(ticket["GwaEvents"]);
          ticket["Win"] = this.convertToReadableNumber(ticket["Win"]);
          ticket["CtrbBets"] = (ticket["CtrbBets"]*100).toFixed(2)+"%";
          ticket["SumWin"] = this.convertToCurrency(ticket["SumWin"]);
          ticket["ggr"] = this.convertToCurrency(
            this.fromCurrencyToFloat(ticket["SumBet"]) -
              this.fromCurrencyToFloat(ticket["SumWin"])
          );

          ticket["margin"] =
            (
              (this.fromCurrencyToFloat(ticket["ggr"]) /
                this.fromCurrencyToFloat(ticket["SumBet"])) *
              100
            ).toFixed(2) + "%";
        });
        this.createOveralls();
        this.mapStakes();
        }
      } else {
        this.tickets = [];
      }
      this.json_data = this.tickets;
      
    },
    prepareAdvanced(data){
      this.assignIds(data);
      this.groupedMatches = _.cloneDeep(data)
      let groupedData = [];
      data.forEach(  
        d => { 
        if( !groupedData[d.MatchId] ){  
            groupedData[d.MatchId] = []; 
        } 
        groupedData[d.MatchId].push(d); 
     }   
    ); 
    let finalData = [];
    let passedFirst = false;
    var sumBet = 0;
    var sumWin = 0;
    var obj = {}
    groupedData.forEach(el=>{
      el.forEach(el2=>{
        if(!passedFirst){
          sumBet+=el2.SumBet
          sumWin+=el2.SumWin
          obj.Date = el2.Date;
          obj.HomeCompetitorName = el2.HomeCompetitorName
          obj.AwayCompetitorName = el2.AwayCompetitorName
          obj.HomeValue = el2.HomeValue
          obj.AwayValue = el2.AwayValue
          obj.BetGameName = el2.BetGameName
          obj.BetGameOutcomeName = el2.BetGameOutcomeName
          obj.MatchId = el2.MatchId
          obj.SlipId = el2.SlipId
          passedFirst=true;
        } else {
          sumBet+=el2.SumBet
          sumWin+=el2.SumWin
        }
      })
      obj.SumBet = sumBet;
      obj.SumWin = sumWin;
      obj.ggr = sumBet-sumWin;
      finalData.push(obj);
      sumBet = 0;
      sumWin = 0;
      passedFirst = false;
      obj = {}
    })
    let ordered = _.orderBy(finalData, ['ggr'], ['asc']);
    ordered.forEach(el=>{
      el['SumWin'] = this.convertToCurrency(el['SumWin']);
      el['SumBet'] = this.convertToCurrency(el['SumBet']);
      el['ggr'] = this.convertToCurrency(el['ggr']);
      el['Date'] = this.formatDate(el['Date'])
    })



    this.tickets = ordered;

    
    },
    assignIds(data){
      data.forEach((el,index)=>{
        el.unique = index+1
      })
    },
    formatDate(date) {
      if(date){
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
    var t = date.split(/[- :]/);
    var d = new Date(t[0]+"-"+t[1]+"-"+t[2])
    let datePrep = new Date(d);
     return datePrep.getDate() + ". " + months[datePrep.getMonth()];
      }
         
    },
    convertToCleanFloat(num) {
      return num.replace("$", "").replace(/,/g, "");
    },
    createOveralls() {
      //c - stands for cumulative
      let cWin = this.tickets.reduce(
        (a, b) => a + this.fromCurrencyToFloat(b["Win"]),
        0
      );
      let cBet = this.tickets.reduce(
        (a, b) => a + this.fromCurrencyToFloat(b["Bet"]),
        0
      );
      let cSumWin = this.tickets.reduce(
        (a, b) => a + this.fromCurrencyToFloat(b["SumWin"]),
        0
      );
      let cSumBet = this.tickets.reduce(
        (a, b) => a + this.fromCurrencyToFloat(b["SumBet"]),
        0
      );
      let cSumGgr = this.tickets.reduce(
        (a, b) => a + this.fromCurrencyToFloat(b["ggr"]),
        0
      );
      this.overalls.win = this.convertToReadableNumber(cWin);
      this.overalls.bet = this.convertToReadableNumber(cBet);
      this.overalls.sumbet = this.convertToCurrency(cSumBet);
      this.overalls.sumwin = this.convertToCurrency(cSumWin);
      this.overalls.sumggr = this.convertToCurrency(cSumGgr);
      this.overalls.marginudeo = 
        this.convertToCurrency((cSumGgr / cSumBet) * 100) + "%";
      this.overalls.avgBetSum = this.convertToCurrency(this.fromCurrencyToFloat(this.overalls.sumbet)/this.fromCurrencyToFloat(this.overalls.bet));
      this.overalls.ctrbSum = (this.fromCurrencyToFloat(this.overalls.win)/this.fromCurrencyToFloat(this.overalls.bet)).toFixed(2)+"%";
    },
    mapStakes() {
      if(this.isDayFiltering()){
        this.tickets.sort((a, b) => (a.Date > b.Date ? 1 : -1));
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
          let datePrep = new Date(tiket["Date"]);
          tiket["Date"] =
            datePrep.getDate() + ". " + months[datePrep.getMonth()];
        });
      } else if(this.isYearFiltering()){
        //stays the same
      } else {
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
          let monthnum = tiket["Date"]
          tiket["Date"] = months[monthnum-1];
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
        if (value!="Date" && value!="margin" && value!="CtrbBets") {
          this.chartFilterData.push({
            id: key,
            title: this.customMapTableHeader(value),
          });
        }
      });
      //labels
      let labels = this.tickets.map((x) => x.Date);
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
            backgroundColor.push(IS_PER_YEAR ? this.random_rgba() : "indianred");
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
            backgroundColor.push(IS_PER_YEAR ? this.random_rgba() : "oceanblue");
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
            backgroundColor.push(IS_PER_YEAR ? this.random_rgba() : "olivegreen");
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
      if(this.chartMode)
      this.forceRender();
    },
    forceRender() {
      this.chartMode = false;
      this.$nextTick(() => {
        this.chartMode = true;
      });
    },
    isYearFiltering(){
       return this.tickets[0]['Date'].toString().length == 4
    },
    isDayFiltering() {
      return (
        this.tickets.filter((x) => x.Date.toString().includes("-")).length > 0
      );
    },
    customMapTableHeader(value) {
      switch (value) {
        case "Bet":
          return "#BET";
        case "SumBet":
          return "ΣBET";
        case "AvgBet":
          return "AVG.BET";
        case "GwaOdds":
          return "GWA.ODDS";
        case "GwaEvents":
          return "GWA.EVENTS";
        case "Win":
          return "#WIN";
        case "CtrbBets":
          return "CTRB.BETS";
        case "SumWin":
          return "ΣWIN";
        case "ggr":
          return "ΣGGR";
        case "margin":
          return "MARGIN";
        case "Date":
          return "Date";
        case "HomeCompetitorName":
          return "Home";
        case "AwayCompetitorName":
          return "Away";
        case "HomeValue":
          return "Home Score";
        case "AwayValue":
          return "Away Score";
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
          text: "Stake",
          align: "start",
          value: "Date",
        },
        {
          text: "#Bet",
          value: "Bet",
        },
        {
          text: "ΣBet",
          value: "SumBet",
        },
        {
          text: "Avg.Bet",
          value: "AvgBet",
        },
        {
          text: "GWA.Odds",
          value: "GwaOdds",
        },
        {
          text: "GWA.Events",
          value: "GwaEvents",
        },
        {
          text: "#Win",
          value: "Win",
        },
        {
          text: "Ctrb.#Bets",
          value: "CtrbBets",
        },
        {
          text: "ΣWin",
          value: "SumWin",
        },
        {
          text: "∑GGR",
          value: "ggr",
        },
        {
          text: "Margin",
          value: "margin",
        },
      ];
    },
    headers2(){
      return [
        {
          text: "Date",
          align: "start",
          value: "Date",
        },
        {
          text:"Home",
          value:"HomeCompetitorName"
        },
        {
          text:"Away",
          value:"AwayCompetitorName"
        },
        {
          text:"Home Score",
          value:"HomeVaue"
        },
        {
          text:"Away Score",
          value:"AwayValue"
        },
        {
          text:"#Bet",
          value:"numberOfBets"
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
          text:"ΣGGR",
          value:"ggr"
        }
      ];
    }
  },
  updated(){

  },
  created() {
    this.determineURL();
    this.tickets = [];
    axios
      .all([axios.get(this.url + "/api/Sport"), axios.get(this.url+"/api/Competition")])
      .then((response) => {
        this.allSports = _.cloneDeep(response[0].data.data);
        this.allCompetitions = _.cloneDeep(response[1].data.data);
        this.sports = this.allSports;
        this.competitions = this.allCompetitions;
        this.competitions = _.cloneDeep(this.competitions.filter(x=>x.cs_id==1));
        this.competitions.unshift({id:0, title:'All Competitions'})
      
      })
      .catch((e) => {
        console.error(e.message);
      });
  },
};
</script>

<style>
.super{
  width:50%!important
}
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
.maxwidth{
  width:100%!important
}
.f14{
  font-size:14px!important
}
.f9{
  font-size:9px!important
}
.v-toolbar__content {
  background-color: #225e0d !important;
}
@media screen and (min-width: 768px) {
  #report1 table {
    border-top: 1px solid black;
  }
  #report1 .mainHeader:nth-child(6),
  #report1 .mainHeader:nth-child(9) {
    border-right: 1px solid black;
  }
  #report1 .mainHeader:nth-child(2) {
    border-left: 1px solid black;
  }
  #report1 .mainHeader:nth-child(3) {
    border-right: 1px solid black;
  }
  #report1 table td + td:nth-child(2),
  #report1 table td + td:nth-child(4),
  #report1 table td + td:nth-child(7),
  #report1 table td + td:nth-child(10),
  #report1 table td + td:nth-child(7) {
    border-left: 1px solid black;
  }
}
@media screen and (max-width: 768px) {
  .super{
  width:100%!important
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
</style>
