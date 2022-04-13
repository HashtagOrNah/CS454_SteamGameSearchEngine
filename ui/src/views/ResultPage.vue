<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="10">
        <v-row style="margin: 2vh; margin-top: 0">
          <v-col cols="3">
            <v-btn color="error" block="true" @click="backToSearch()">
              Back to Search
            </v-btn>
          </v-col>
          <v-col cols="6">
          </v-col>
          <v-col cols="3">
            <v-btn color="secondary" block="true" @click="isFilter=true">
              Filter Results
            </v-btn>
          </v-col>
        </v-row>
        <v-row v-for="item in results" :key="item.id">
          <v-col>
            <v-card @click="snackbar = true; sbtext = item.id" density="compact">
              <v-row no-gutters align="center">
                <v-col cols="2">
                  <v-avatar
                      class="ma-3"
                      size="125"
                      rounded="0"
                  >
                    <v-img :src="item.img"></v-img>
                  </v-avatar>
                </v-col>
                <v-col cols="2">
                  <v-card-title class="text-h4">
                    {{ item.title }}
                  </v-card-title>
                </v-col>
                <v-col cols="8">
                  <v-card-content>
                    {{ item.desc }}
                  </v-card-content>
                </v-col>
              </v-row>
            </v-card>
          </v-col>
        </v-row>
        <v-row style="margin: 1vh">
          <v-col cols="2" @click="prevPage()">
            <v-btn block="true">
              Previous
            </v-btn>
          </v-col>
          <v-col cols="8">
          </v-col>
          <v-col cols="2" @click="nextPage()">
            <v-btn block="true">
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
    }
  },
  data: () => ({
    isFilter: false,
    snackbar: false,
    sbtext: "",
    results: [],
  }),
  computed: {

  },
  mounted() {
    let {_, ...params} = this.$route.query;
    _;
    fetch(`${location.origin}/api/search?${new URLSearchParams(params)}`)
      .then(resp => resp.json())
      .then(data => (this.results = data.results));
  }
}
</script>

<style scoped>

</style>