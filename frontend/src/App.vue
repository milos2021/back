<template>
  <v-app>
    <v-app-bar app color="primary" v-if="orientationMode != 'landscape'" dark>
      <v-container fluid>
        <v-row align="center" class="mobileHidden">
          <v-col class="d-flex" cols="3" sm="12">
            <v-img
              alt="Soccer Reporting"
              class="shrink mt-1 hidden-sm-and-down"
              contain
              min-width="100"
              src="@/assets/soccerLogo.svg"
              width="100"
            />
          </v-col>
        </v-row>
        <v-row align="center">
          <v-col class="d-flex" cols="4" sm="12" id="list">
            <v-select
              v-model="selectedReport"
              v-on:change="switchReport"
              :items="reports"
              color="blue-grey lighten-2"
              label="Select report"
              item-text="name"
              item-value="name"
            >
              <template slot="item" slot-scope="data">
                <!-- Divider and Header-->
                <template v-if="typeof data.item !== 'object'">
                  <v-list-item-content v-text="data.item" />
                </template>
                <!-- Normal item -->
                <template v-else>
                  <v-list-item-content>
                    <v-list-item-title v-html="data.item.name" />
                  </v-list-item-content>
                </template>
              </template>
            </v-select>
          </v-col>
        </v-row>
        <v-row align="center" class="mobileHidden">
          <v-col class="d-flex" cols="2" sm="12"> </v-col>
        </v-row>
        <v-row align="center" class="mobileHidden" id="version">
          <v-col
            class="d-flex"
            cols="3"
            sm="12"
            style="margin-bottom: 17px; flex: none"
          >
            <v-btn href="#" target="_blank" text>
              <span class="mr-2">Reporting v1.0</span>
            </v-btn>
            <img
              v-on:click="logout"
              src="@/assets/logout.png"
              style="
                width: 18px;
                height: 18px;
                margin-top: 9px;
                cursor: pointer;
              "
            />
          </v-col>
        </v-row>
      </v-container>

      <v-spacer></v-spacer>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
    <div class="loading">
      <div class="uil-ring-css" style="transform: scale(0.79)">
        <div></div>
      </div>
    </div>
  </v-app>
</template>

<script>
import OrientationService from "./services/orientation.service";
const axios = require("axios").default;
export default {
  name: "App",

  data: () => ({
    url:"http://10.0.90.23",
    orientationMode: null,
    initialLoad: OrientationService.getInitialLoad(),
    selectedReport: "Basic",
    reports: [
      { header: "Betting" },
      { name: "Basic", group: "Betting" },
     // { name: "Sport", group: "Betting" },
      { name: "Rep Stats", group: "Betting" },
      { divider: true },
      { header: "Cashflow" },
      { name: "Report 2", group: "Cashflow" },
     // { divider: true },
     // { header: "Slips" },
     // { name: "Detailed Preview", group: "Slips" },
     // { divider: true },
     // { header: "Users" },
     // { name: "Advanced Statistic For Period", group: "Users" },
    ],
  }),
  watch: {
    $route(to, from) {
      console.log([to, from]);
      // react to route changes...
    },
  },
  methods: {
    logout() {
      let token = JSON.parse(localStorage.getItem("token"));

      axios
        .post(this.url+"/api/session", {logout:true, token})
        .then((response) => {
          console.log(response)
          window.location.href = this.url;
          localStorage.removeItem("token");
        });
    },
    handleOrientationChange() {
      var mql = window.matchMedia("(orientation: portrait)");
      var that = this;
      mql.addListener(function (m) {
        if (m.matches) {
          that.$nextTick(() => {
            that.orientationMode = "portrait";
          });
        } else {
          that.$nextTick(() => {
            that.orientationMode = "landscape";
          });
        }
        that.initialLoad = OrientationService.getInitialLoad();
      });
    },
    switchReport(event) {
      switch (event) {
        case "Basic":
          this.$router.replace("/reporting/Tiket");
          break;
        case "Sport":
          this.$router.replace("/reporting/Sport");
          break;
        case "Rep Stats":
          this.$router.replace("/reporting/RepStats");
          break;
        case "Report 2":
          this.$router.replace("/reporting/Cashflow");
          break;
        case "Detailed Preview":
          this.$router.replace("/reporting/SlipDetailedPreview");
          break;
        case "Advanced Statistic For Period":
          this.$router.replace("/reporting/AdvancedStatisticForPeriod");
          break;
        default:
          break;
      }
    },
  },
  // beforeRouteUpdate(to, from, next) {
  //   console.log([to, from, next]);
  // },
  created() {
    let token = JSON.parse(localStorage.getItem("token"));
    if (token) {
      //verifying token
      axios
        .post(this.url+"/api/session", { token })
        .then((response) => {
          var ok = response.status == 200;
              var loadingOverlay = document.querySelector(".loading");
          if (ok) {
            loadingOverlay.classList.add("hidden");
          } else {
            window.location.href = this.url;
          }
        });
    } else {
      window.location.href = this.url;
    }

    this.handleOrientationChange();
    let path = this.$route.fullPath;
    switch (path) {
      case "/reporting/Tiket":
        this.selectedReport = "Basic";
        break;
      case "/reporting/Sport":
        this.selectedReport = "Sport";
        break;
      case "/reporting/Cashflow":
        this.selectedReport = "Report 2";
        break;
      case "/reporting/RepStats":
        this.selectedReport = "Rep Stats";
        break;
      case "/reporting/SlipDetailedPreview":
        this.selectedReport = "Detailed Preview";
        break;
      case "/reporting/AdvancedStatisticForPeriod":
        this.selectedReport = "Advanced Statistic For Period";
        break;
      default:
        break;
    }
  },
};
</script>
<style>
/* spinner */
/* spinner */
*.hidden {
  display: none !important;
}

div.loading {
  z-index: 100;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(16, 16, 16, 0.5);
}

@-webkit-keyframes uil-ring-anim {
  0% {
    -ms-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -ms-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@-webkit-keyframes uil-ring-anim {
  0% {
    -ms-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -ms-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@-moz-keyframes uil-ring-anim {
  0% {
    -ms-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -ms-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@-ms-keyframes uil-ring-anim {
  0% {
    -ms-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -ms-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@-moz-keyframes uil-ring-anim {
  0% {
    -ms-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -ms-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@-webkit-keyframes uil-ring-anim {
  0% {
    -ms-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -ms-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@-o-keyframes uil-ring-anim {
  0% {
    -ms-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -ms-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@keyframes uil-ring-anim {
  0% {
    -ms-transform: rotate(0deg);
    -moz-transform: rotate(0deg);
    -webkit-transform: rotate(0deg);
    -o-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -ms-transform: rotate(360deg);
    -moz-transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
    -o-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
.uil-ring-css {
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  width: 200px;
  height: 200px;
}
.uil-ring-css > div {
  position: absolute;
  display: block;
  width: 160px;
  height: 160px;
  top: 20px;
  left: 20px;
  border-radius: 80px;
  box-shadow: 0 6px 0 0 #ffffff;
  -ms-animation: uil-ring-anim 1s linear infinite;
  -moz-animation: uil-ring-anim 1s linear infinite;
  -webkit-animation: uil-ring-anim 1s linear infinite;
  -o-animation: uil-ring-anim 1s linear infinite;
  animation: uil-ring-anim 1s linear infinite;
}

.v-main {
  background-image: url("assets/bg.jpg");
  background-size: cover;
}
#version {
  flex: none;
}
.mobileHidden {
  display: flex;
}
.v-subheader {
  font-weight: bold !important;
}
.v-list-item__content {
  padding-left: 20px !important;
}
@media screen and (max-width: 768px) {
  .mobileHidden {
    display: none !important;
  }
  #list .v-input {
    max-width: fit-content !important;
  }
}
@import "https://unpkg.com/bootstrap/dist/css/bootstrap.min.css";
</style>
