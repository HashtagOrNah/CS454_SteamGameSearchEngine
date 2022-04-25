<template>
  <v-dialog v-model="dialog">
    <v-card>
      <v-card-title>Sort by Field</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <v-radio-group v-model="rerankPending">
          <v-radio
              v-for="i in reranks"
              :key="i.value"
              :label="i.text"
              :value="i"
          ></v-radio>
        </v-radio-group>
      </v-card-text>
      <v-divider></v-divider>
      <v-progress-linear indeterminate v-if="loading"></v-progress-linear>
      <v-card-actions>
        <v-btn color="secondary" text :disabled="loading" @click="dialog = false"> Close</v-btn>
        <v-btn color="primary" text :disabled="loading" @click="runRerank()"> Save</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
  <v-container fluid style="min-height: calc(100vh - 80px)">
    <v-row justify="center">
      <v-col cols="10">
        <v-row style="margin: 2vh; margin-top: 0">
          <v-col cols="3">
            <v-btn color="error" block="true" @click="backToSearch()">
              Back to Search
            </v-btn>
          </v-col>
          <v-col cols="4" offset="1">
            <v-expand-transition>
              <div v-if="rerank.value !== ''">
                <v-btn variant="outlined" block="true" @click="resetRerank()">
                  Sort by: {{ rerank.text }}
                </v-btn>
              </div>
            </v-expand-transition>
          </v-col>
          <v-col cols="3" offset="1">
            <v-btn color="primary" block="true" @click="dialog=true">
              Sort Results
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            Results: {{ resultCount }}
          </v-col>
        </v-row>
        <v-row v-for="item in results" :key="item.id" style="margin: -4px">
          <v-col>
            <v-card @click="loadDetails(item.id)" density="compact">
              <v-row no-gutters align="center">
                <v-col cols="2" align="center">
                  <v-avatar
                      class="ma-3"
                      size="150"
                      rounded="0"
                  >
                    <v-img :src="item.img"></v-img>
                  </v-avatar>
                </v-col>
                <v-col cols="3">
                  <v-card-title class="text-h4" style="line-height: 2.5rem">
                    {{ item.title }}
                  </v-card-title>
                </v-col>
                <v-col cols="7">
                  <v-card-content>
                    <div v-html="item.desc"></div>
                  </v-card-content>
                </v-col>
              </v-row>
              <v-divider></v-divider>
              <v-row>
                <v-col cols="3">
                  Release Date: {{ item.date }}
                </v-col>
                <v-col cols="3">
                  Review Count: {{ item.reviews }}
                </v-col>
                <v-col cols="3">
                  Achievement Count: {{ item.achievements }}
                </v-col>
                <v-col cols="3">
                  Full Price: {{ getPriceStr(item.price) }}
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>
        <v-row style="margin: 1vh">
          <v-col cols="2">
            <v-btn block="true" :disabled="pageNum <= 1" @click="prevPage()">
              Previous
            </v-btn>
          </v-col>
          <v-col cols="2" offset="3">
            <v-btn v-if="pageNum >= 2" variant="outlined" color="error" block="true" @click="firstPage()">
              Return to page 1
            </v-btn>
          </v-col>
          <v-col cols="2" offset="3">
            <v-btn block="true" :disabled="isLast" @click="nextPage()">
              Next
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
  <v-snackbar v-model="snackbar" :timeout="2000" color="surface">
    <div class="">
      clicked on item {{ sbtext }}!
    </div>
    <template v-slot:actions>
      <v-btn color="primary" variant="text" @click="snackbar = false">
        Close
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  name: "ResultsPage",
  methods: {
    backToSearch() {
      this.$router.push({path: "/", query: this.$route.query})
    },
    getPriceStr(price) {
      if (price < 0) return "Free"
      let real_price = price / 100
      real_price = real_price.toLocaleString("en-US", {style: "currency", currency: "USD"})
      return real_price
    },
    prevPage() {
      this.pageNum -= 1
      const url = new URL(window.location)
      url.searchParams.set('pagenum', this.pageNum)
      window.history.pushState({}, '', url)
      this.loadResults()
    },
    firstPage() {
      this.pageNum = 1
      const url = new URL(window.location)
      url.searchParams.set('pagenum', this.pageNum)
      window.history.pushState({}, '', url)
      this.loadResults()
    },
    nextPage() {
      this.pageNum += 1
      const url = new URL(window.location)
      url.searchParams.set('pagenum', this.pageNum)
      window.history.pushState({}, '', url)
      this.loadResults()
    },
    loadDetails(gid) {
      this.$router.push({path: `/detail/${gid}`})
    },
    resetRerank() {
      this.rerankPending = this.reranks[0]

      this.runRerank()
    },
    runRerank() {
      this.loading = true

      const url = new URL(window.location)
      if (this.rerankPending.value !== '') {
        url.searchParams.set('sortby', this.rerankPending.value)
      } else {
        url.searchParams.delete('sortby')
      }
      window.history.pushState({}, '', url)


      fetch(`${location.origin}/api/search?${url.searchParams}`)
          .then(resp => resp.json())
          .then(data => {
            this.results = data.results
            this.resultCount = data.result_count
            this.isLast = data.is_last_page
          }).finally(() => {
        this.rerank = this.rerankPending
        this.loading = false
        this.dialog = false

      });
    },
    loadResults() {
      const url = new URL(window.location)
      fetch(`${location.origin}/api/search?${url.searchParams}`)
          .then(resp => resp.json())
          .then(data => {
            this.results = data.results
            this.resultCount = data.result_count
            this.isLast = data.is_last_page
          });
    }
  },
  data: () => ({
    loading: false,
    isFilter: false,
    snackbar: false,
    sbtext: "",
    results: [],
    resultCount: 0,
    pageNum: 1,
    isLast: false,
    query: "",
    dialog: false,
    rerank: {text: "No Sorting", value: ""},
    rerankPending: {text: "No Sorting", value: ""},
    reranks: [
      {text: "No Sorting", value: ""},
      {text: "Price (ASC)", value: "price-asc"},
      {text: "Price (DESC)", value: "price-desc"},
      {text: "Title (ASC)", value: "title-asc"},
      {text: "Title (DESC)", value: "title-desc"},
      {text: "Release Date (ASC)", value: "date-asc"},
      {text: "Release Date (DESC)", value: "date-desc"},
      {text: "Review Count (ASC)", value: "reviews-asc"},
      {text: "Review Count (DESC)", value: "reviews-desc"},
      {text: "Achievement Count (ASC)", value: "achievements-asc"},
      {text: "Achievement Count (DESC)", value: "achievements-desc"},
    ],
  }),
  computed: {},
  mounted() {
    let {_, ...params} = this.$route.query;
    _;
    this.query = params.q
    let pagenum = parseInt(params.pagenum)
    if (pagenum > 1) {
      this.pageNum = pagenum
    }
    this.loadResults()
  }
}
</script>

<style scoped>

</style>