<template>
  <div>
    <v-container fluid>
      <v-row align="center">
        <v-col cols="1" sm="1" style="margin-top:20px">
          <v-text-field
            @keyup.native="checkIfEligible"
            @change.native="checkIfEligible"
            v-model="ticketId"
            label="Ticket ID here"
            solo-inverted
          ></v-text-field>
        </v-col>
        <v-col cols="1" sm="1" style="margin-top:22px">
          <v-btn
            class="btnSearch"
            :disabled="isError"
            elevation="2"
            outlined
            plain
            raised
            v-on:click="getData"
            >Search</v-btn
          >
        </v-col>
        <v-col cols="10" sm="10" class="mtop3" v-if="loadingData!=null && loadingData!=true && data.length>0">
        <v-container
          class="ticket"
          style="width:60%"
        >
          <table 
            style="margin-top:15px; color:white; width:100%"
          >
            <tr>
              <td>
                <p>
                  TIKET JE:
                  {{ globalTicketData.Status == 1 || globalTicketData.Status==2 ? "DOBITAN" : "GUBITAN" }}&nbsp;
                   <img v-if="globalTicketData.Status>=1" src="@/assets/ok.png" style="margin-top:-3px; margin-left:4px" width="15"/>
                   <img v-if="globalTicketData.Status==-1" src="@/assets/notok.png" style="margin-top:-3px; margin-left:4px" width="15"/>
                </p>
              </td>
              <td>
                <p style="text-align:right">
                  {{getTicketType()}} TIKET
                </p>
              </td>
            </tr>
            <tr>
              <td>
                <p>
                  #{{ globalTicketData.SlipId }}, Korisnik:
                  {{ globalTicketData.User }} {{globalTicketData.Location ? '('+globalTicketData.Location+')' : ''}}
                </p>
              </td>
              <td style="text-align:right">
                <p>VREME UPLATE: {{ globalTicketData.DatePaid }}</p>
              </td>
            </tr>
          </table>

          <table class="table" id="glavna"
            style="padding-right:40px; padding-left:40px; color:white; width:100%"
          >
            <thead>
              <tr>
                <td>Početak</td>
                <!-- <td>Match Code</td> -->
                <td>Competition</td>
                <td></td>
                <td>Dogadjaj</td>
                <td>Igra</td>
                <td>Kvota</td>
                <td>O/C</td>
                <!-- <td></td> -->
                <td>Rezultat</td>
                <td></td>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="item in data"
                v-bind:key="item.MatchId"
              >
              <!--
                 :style="[
                  item.MatchStatus == -1
                    ? { background: 'red' }
                    : { background: 'green' },
                ]"
              -->
                <td class="CellWithComment" style='width:100px'><v-container class="colPrikaz"><span>{{getDate(item.StartDate)}}</span>
                    <span>{{getDayOfWeekAndTime(item.StartDate)}}</span></v-container>
                    <span class="CellComment">{{item.MatchCode}}</span>
                </td><!-- false II param za prikaz godine, III param za prikaz sekundi -->
                <!-- <td style='width:120px'>
                  {{ item.MatchCode }}
                  <span v-if='item.BetType==2'>
                   <img src="@/assets/live.png" class="live" width="13"/>
                  </span>
                </td> -->
                <td style='width:140px'>
                  <v-container class="colPrikaz">
                    <span>
                      <img v-if="item.SportId==1" src="@/assets/football.png" style="margin-top:-4px" width='16'/>
                  <img v-if="item.SportId==2" src="@/assets/basketball.png" style="margin-top:-4px" width='16'/>
                  <img v-if="item.SportId==3" src="@/assets/tennis.png" style="margin-top:-4px" width='16'/>
                  {{getSportName(item.SportId)}}
                    </span>
                    <span>{{item.CompetitionName}}</span>
                  </v-container>
                </td>
                <td style="vertical-align:middle; position:relative" >
                  <span v-if='item.BetType==2' >
                    <p class="liveobr">LIVE</p>
                   <!-- <img src="@/assets/live.png" class="live" width="13"/> -->
                  </span>
                </td>
                <td style='width:170px'><v-container class="colPrikaz"><span>{{item.Home}}</span>
                    <span>{{item.Away}}</span></v-container></td>
                <td style='width:140px'>
                <v-container class="colPrikaz">
                <span>{{item.BetGameName}}</span>
                <span>{{ item.Game }} {{item.Param ? '('+item.Param+')' : ''}}</span>
                </v-container>
                </td>
                <td style='width:100px; vertical-align:middle'><span class="stilKv">{{ item.OddsPlayed.toFixed(2) }}</span></td>
                <td style='width:100px'>
                  <!--:style="[
                  item.OpeningOdds>item.OddsPlayed
                    ? { color: 'green' }
                    : (item.OpeningOdds==item.OddsPlayed ? { color: 'white' } : { color: 'red' }),
                  ]"-->
                  <div style="display:flex">
                  <v-container class="colPrikaz">
                  <span
                  style="color:white"
                  >{{ item.OpeningOdds == 0 ? '' : item.OpeningOdds.toFixed(2) }}</span>
                  <span
                  :style="[
                  item.ClosingOdds>item.OddsPlayed
                    ? { color: 'green' }
                    : (item.ClosingOdds==item.OddsPlayed ? { color: 'white' } : { color: 'red' }),
                  ]"
                  >{{ item.ClosingOdds == 0 ? '' : item.ClosingOdds.toFixed(2) }}
                  </span>
                  </v-container>
                  <v-container class="colPrikaz">
                    <span v-if="item.OpeningOdds>item.ClosingOdds && item.ClosingOdds" style='font-size:25px; color:red; text-align:center'>
                    &darr;
                  </span>
                  <span v-if="item.OpeningOdds<item.ClosingOdds && item.ClosingOdds" style='font-size:25px; color:green; text-align:center'>
                    &uarr;
                  </span>
                  <span v-if="item.OpeningOdds==item.ClosingOdds && item.ClosingOdds" style='font-size:25px; color:white; text-align:center'>
                    &harr;
                  </span>
                  </v-container>
                  </div>
                </td>
                <!-- <td style="width:50px">
                  
                </td> -->
                                <td style='width:120px'>
                    <div style='display:flex' v-html='getAdditional(item)'></div>
                </td>
                  <td>
                   <img v-if="item.MatchStatus>0" src="@/assets/ok.png" style="margin-top:15px" width="15"/>
                   <img v-if="item.MatchStatus==-1" src="@/assets/notok.png" style="margin-top:15px" width="15"/>
                </td>
              </tr>
            </tbody>
          </table>
          <table class="table"
            style="padding-top:20px;padding-right:40px; padding-left:40px; color:white; width:100%"
          >
            <tr>
              <td>UPLATA</td>
              <td>{{ convertToCurrency(globalTicketData.AmountPaid) }}</td>
              <td>DOBITAK</td>
              <td>{{ convertToCurrency(globalTicketData.Win) }}</td>
            </tr>
            <tr>
              <td>UKUPNA KVOTA</td>
              <td>{{ convertToCurrency(globalTicketData.SumOdds) }}</td>
              <td>BONUS</td>
              <td>{{ convertToCurrency(globalTicketData.BonusWin) }}</td>
            </tr>
            <tr>
              <td>BROJ PAROVA</td>
              <td>{{ globalTicketData.numberOfMatches }}</td>
              <td>UKUPNA ISPLATA</td>
              <td>
                {{
                  convertToCurrency(
                    globalTicketData.Win + globalTicketData.BonusWin
                  )
                }}
              </td>
            </tr>
          </table>
        </v-container>
        </v-col>
      </v-row>
    </v-container>
    <v-container fluid v-if="data.length == 0 || loadingData==true">
      <v-row align="center">
        <v-col cols="3" sm="3"></v-col>
        <v-col cols="6" sm="6" class="mtop10">
          <span v-if="loadingData==null">Ticket will load here</span>
          <v-container v-if="loadingData">
            <loading :active.sync="loadingData" 
            loader="dots"
            color="#225e0d"
            blur="10px"
        :is-full-page="fullPage"></loading>
          </v-container>
        </v-col>
        <v-col cols="3" sm="3"></v-col>
      </v-row>
    </v-container>
    <v-container fluid v-if="data.length > 0">
      <v-row align="center">
        
        <v-col cols="2" sm="2"></v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
// Import component
    import Loading from 'vue-loading-overlay';
    // Import stylesheet
    import 'vue-loading-overlay/dist/vue-loading.css';
// var _ = require('lodash');
import { targetURL } from "../global/config";
// import Bar from "../views/charts/Bar.vue";
const axios = require("axios").default;
export default {
  name: "slipdetailedpreview",
  data() {
    return {
      loadingData: null,
      fullPage:true,
      ticketId: null,
      isError: true,
      globalTicketData: {},
      data: [],
      months: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "Maj",
        "Jun",
        "Jul",
        "Avg",
        "Sep",
        "Okt",
        "Nov",
        "Dec",
      ],
    };
  },
  components:{
    Loading
  },
  methods: {
    getTicketType(){
      switch(this.globalTicketData.SlipType){
        case 0:
          return "PREMATCH"
        case 1:
          return "LIVE"
        case 2:
          return "MIXED"
        case 3:
          return "OUTRIGHT"
        default:
          return "UNKNOWN TYPE"
      }
    },
    getSportName(sportId){
      switch(sportId){
        case 1:
          return "Fudbal";
        case 2:
          return "Košarka";
        case 3:
          return "Tenis";
        case 4:
          return "Rukomet";
        case 5:
          return "Odbojka";
        case 6:
          return "Hokej";
        case 7: 
          return "Bejzbol";
        case 9:
          return "Vaterpolo";
        case 10:
          return "Americki fudbal";
        case 11:
          return "Golovi u ligi";
        case 12:
          return "Igrači specijal";
        case 13:
          return "Dueli timova";
        case 14:
          return "Futsal";
        case 15:
          return "Meč specijal";
        case 16:
          return "Specijal";
        case 17:
          return "Olimpijske igre";
        case 18:
          return "Košarka specijal";
        case 19:
          return "Odbojka specijal";
        case 20:
          return "Rukomet specijal";
        case 21:
          return "ZOI 2018 specijal";
        case 22:
          return "Dueli strelaca";
        case 23:
          return "Zimski sportovi";
        case 24:
          return "3x3 košarka";
        case 25:
          return "Stoni tenis";
        case 26:
          return "Borilačke veštine";
        case 27:
          return "Australijski fudbal";
        case 28:
          return "ESport";
        case 29:
          return "Pikado";
        case 30:
          return "Šah";
        case 31:
          return "Snuker";
        case 34:
          return "Politika";
      }

    },
    getAdditional(item){
      var str = "";
      if(item.halftime){
        str+="(";
        str+=item.halftime;
        if(item.periods==""){
          str+=")"
        } else {
          str+=","
          if(item.periods.slice(-1)===","){
            item.periods = item.periods.slice(0,-1)
          }
          str+=item.periods;
          str+=")"
        }
      } else {
        if(item.periods!=""){
          str+="(";
          if(item.periods.slice(-1)===","){
            item.periods = item.periods.slice(0,-1)
          }
          str+=item.periods;
          str+=")"
        }
      }
      let sportsWithOvertime = [1,2,50];
      let sportsWithPenalties = [1];
      if(sportsWithOvertime.includes(item.SportId) && item.overtime){
        str = str.slice(0,-1);
        str+=","
        str+=item.overtime
        str+=")"
      }
      if(sportsWithPenalties.includes(item.SportId) && item.penalties){
        str = str.slice(0,-1);
        str+=","
        str+=item.penalties
        str+=")"
      }

      let strRemovedBrackets = str.substring(1,str.length-1); // "1:2,2:3,3:4"
      let strToArray = strRemovedBrackets.split(","); // ["1:2","2:3","3:4"]
      let html = "";
      for(let i=0; i<strToArray.length; i++){
        let domacin = strToArray[i].split(":")[0];
        let gost = strToArray[i].split(":")[1];
        if(item.SportId==3 || item.SportId == 5){ //tenis ili odbojka
          if(parseInt(domacin)>parseInt(gost)){
            html+=
            `
            <v-container style='margin-right:10px' class="colPrikaz">
                <span style='font-weight:bold'>`+domacin+`</span>
                <span>`+gost+`</span>
            </v-container>
            `
          } else {
            html+=
            `
            <v-container style='margin-right:10px' class="colPrikaz">
                <span>`+domacin+`</span>
                <span style='font-weight:bold'>`+gost+`</span>
            </v-container>
            `
          }
        } else {
        html+=
         `
         <v-container style='margin-right:10px' class="colPrikaz">
            <span>`+domacin+`</span>
            <span>`+gost+`</span>
         </v-container>
         `
        }
         
      }
      let pre = `<v-container style='margin-right:10px' class="colPrikaz"><span class="score">`+item.HomeScore+`</span>
                    <span class="score">`+item.AwayScore+`</span></v-container>`
      return pre+html;
    },
    convertToCurrency(value) {
      const formatter = new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        minimumFractionDigits: 2,
      });
      return formatter.format(value).replace("$", "");
    },
    determineURL() {
      let path = window.origin;
      if (path.includes("localhost")) {
        this.url = targetURL.LOCAL;
      } else {
        this.url = targetURL.SERVER;
      }
    },
    checkIfEligible() {
      this.isError = !/^\d{1,}$/.test(this.ticketId);
    },
    // /92863654
    getData() {
      this.isError = false;
      let obj = {
        ticketId: this.ticketId,
      };
      this.loadingData = true;
      axios
        .post(this.url + "/api/SlipDetailedPreview", obj)
        .then((response) => {
          if(response.data.tiket.length>0){
                      this.loadingData = false;
          this.checkForNulls(response.data.tiket);
          this.data = response.data.tiket;
          this.assignGlobalPropsToData(this.data[0]);
          this.formatTicket(this.data);
          } else {
            this.data = []
            this.loadingData = null;
          }

        });
    },
    formatTicket(data){
      let fts = [4,11,17,19,25,29,39,45,52,56,59,60,63,77,79,80,81,82,84,85,87,88,89,90,91,92,93,101,102,103,106] //videti za 56
      let scores = [1,4,5,6,7,8,9,10,11,12,13,14,15,19,20,21,22,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43]
      let dataToDisplay = data.filter(x=>fts.includes(x.MatchPeriodId) && scores.includes(x.DataTypeId));
      this.data = dataToDisplay;
      let notImplemented = [];
      for(let i=0; i<this.data.length;i++){
        this.data[i]['periods'] = "";
        for(let j=0; j<data.length; j++){
          if(this.data[i].MatchId == data[j].MatchId){
            if(scores.includes(data[j].DataTypeId)){
              switch(data[j].MatchPeriodId){
                //poluvremena
                case 3:
                case 18:
                case 62:
                case 78:
                this.data[i]['halftime'] = data[j].HomeScore+":"+data[j].AwayScore
                break;
                //produzeci
                case 53:
                case 9:
                case 50:
                this.data[i]['overtime'] = data[j].HomeScore+":"+data[j].AwayScore
                break;
                //penali
                case 54:
                this.data[i]['penalties'] = data[j].HomeScore+":"+data[j].AwayScore
                break;
                case 5:
                case 6:
                case 7:
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 8:
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore
                break;
                case 12:
                if(data[j].HomeScore && data[j].AwayScore){
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                }
                break;
                case 13:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 14:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 15:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 16:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore
                break;
                case 20:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 21:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 22:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 23:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 24:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore
                break;
                case 26:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 27:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 28:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore
                break;
                case 30:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 31:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 32:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 33:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 34:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 35:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 36:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 37:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 38:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore
                break;
                case 40:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 41:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 42:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 43:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore
                break;
                case 46:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 47:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 48:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 49:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore
                break;
                case 94:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 95:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 96:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 97:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore+","
                break;
                case 98:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore
                break;
                case 99:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore
                break;
                case 100:
                if(data[j].HomeScore && data[j].AwayScore)
                this.data[i]['periods']+=data[j].HomeScore+":"+data[j].AwayScore
                break;
                default:
                  console.log("those should be real matches")
                  notImplemented.push(data[j])
                break;
              }
            }
          }
        }
      }
      this.data = [...this.data]
      
    },
    checkForNulls(data){
      data.forEach(el=>{
        Object.keys(el).forEach(key=>{
          if(el[key]==null){
            el[key]=0.00
          }
        })
      })
    },
    getDate(datetime){
      let datetimeArr = datetime.split(" ");
      let date = new Date(datetimeArr[0]);
      let dateString;
      dateString = date.getDate() + ". " + this.months[date.getMonth()];
      return dateString;
    },
    getDayOfWeekAndTime(datetime){
      var daysOfWeek = [
        "Ned","Pon","Uto","Sre","Čet","Pet","Sub"
      ]
      let datetimeArr = datetime.split(" ");
      let date = new Date(datetimeArr[0]);
      let dayOfWeek = daysOfWeek[date.getDay()];
      let timeParts = datetimeArr[1].split(".")[0].split(":");
      let time = timeParts[0] + ":" + timeParts[1];
      return dayOfWeek+", "+time
    },
    convertToReadableFormat(datetime, includeYear = true, includeSeconds = false) {
      let datetimeArr = datetime.split(" ");
      let date = new Date(datetimeArr[0]);
      let dateString, time;
      if (includeYear) {
        dateString =
          date.getDate() +
          ". " +
          this.months[date.getMonth()] +
          " " +
          date.getFullYear() +
          ".";
        time = datetimeArr[1].split(".")[0];
      } else {
        dateString = date.getDate() + ". " + this.months[date.getMonth()];
        let timeParts = datetimeArr[1].split(".")[0].split(":");
        if(includeSeconds){
          time = timeParts[0] + ":" + timeParts[1]+ ":" + timeParts[2];
        } else {
          time = timeParts[0] + ":" + timeParts[1];
        }
      }

      return dateString + " " + time;
    },
    assignGlobalPropsToData(data) {
      let obj = this.globalTicketData;
      obj["SlipType"] = data.SlipType;
      obj["SlipId"] = data.SlipId;
      obj["DatePaid"] = this.convertToReadableFormat(data.DatePaid);
      obj["User"] = data.Username;
      obj["AmountPaid"] = data.AmountPaid;
      obj["Win"] = data.Win;
      obj["BonusWin"] = data.BonusWin;
      obj["Status"] = data.Status;
      obj['numberOfMatches'] = data.NumberOfMatches;
      obj['SumOdds'] = data.SumOdds
    },
  },
  created() {
    this.determineURL();
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
/* .stilKv{
      background: #c9cd55;
    border: 1px solid black;
    color: black;
    padding: 6px;
    font-weight: bold;
} */
#glavna tbody td {
    border-top:none!important;
    padding-bottom:10px!important
}
#glavna thead td{
  border-bottom:1px solid #dee2e6
}

.liveobr{
  position: absolute;
    top: 8px;
    right: -9px;
      width: 33px;
    transform: rotate( 
-90deg
 );
    margin-top: 8px;
    text-align: center;
    /* vertical-align: middle; */
    color: white;
    background-color: red;
    /* padding: 3px; */
    height: 15px;
    margin-top: 13px;
    font-size: 11px;
    /* font-family: 'Arial';*/
}
.CellWithComment{
  position:relative;
}

.CellComment{
text-align: center;
    display: none;
    position: absolute;
    z-index: 100;
    border: 1px;
    background-color: black;
    border-style: solid;
    border-width: 1px;
    border-color: yellow;
    padding: 3px;
    color: yellow;
    top: 4px;
    left: 0;
    width: 80px;
    height: 50px;
    padding-top: 12px;
}

.CellWithComment:hover span.CellComment{
  display:block;
}
.table td{
  padding:0.35rem
}
.colPrikaz{
  display:flex!important;
  flex-direction: column!important;
  padding:0!important;
}
.score{
  color:yellow
}
.live{
  margin-bottom: 3px;
  margin-left:5px
}
.ticket {
  background-color:black;
  height: auto !important;
  margin-top: 15px;
  border-radius: 5px;
}
.btnSearch {
  margin-top: 0px !important;
  height: 47px !important;
}
/* .mtop3 {
  margin-top: 3%;
} */
.mtop3 v-text-field {
  font-family: "Century Gothic";
}
.mtop10 {
  margin-top: 10%;
  text-align: center;
  font-size: 33px;
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
  #report2 .mainHeader:nth-child(13) {
    border-right: 1px solid black;
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
.v-application .align-center{
  align-items: initial!important;
}
table{
  width:100%
}
</style>
