<template>
  <v-container fluid>
    <v-row>
      <v-col cols="10" offset="1">
        <v-row>
          <v-col cols="2">
            <v-btn color="error" block="true" @click="back()">
              Back to Results
            </v-btn>
          </v-col>
          <v-col cols="8">
            <v-card>
              <v-card-text align="center" class="text-h3" style="line-height: 3.125rem;">
                {{ details.title }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="9">
            <v-row>
              <v-col>
                <v-card align="center">
                  <div style="height: 1rem"></div>
                  <v-img width="80%" :src="details.image_url"></v-img>
                  <div style="height: 1rem"></div>
                </v-card>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-card>
                  <v-card-text>
                    <div style="padding-left: 1rem; padding-right: 1rem">
                      <div v-html="details.about_the_game"></div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-card>
                  <v-card-text>
                    calculated prices
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="3">
            <v-row>
              <v-col>
                <v-card>
                  <v-card-text>
                    Steam Listed Price: {{ getPriceStr(this.details.full_price) }}
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-card>
                  <v-card-text>
                    Genres: {{ this.details.genres }}
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-card>
                  <v-card-text>
                    Developer(s): {{ this.details.developers }}
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-card>
                  <v-card-text>
                    Publisher(s): {{ this.details.publishers }}
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-card>
                  <v-card-text>
                    Link To Original Page
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
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
    back() {
      this.$router.go(-1)
    },
    getPriceStr(price) {
      let real_price = price / 100
      real_price = real_price.toLocaleString("en-US", {style:"currency", currency:"USD"})
      return real_price
    }
  },
  data: () => ({
    snackbar: false,
    sbtext: "",
    details: {},
    prices: [],
  }),
  mounted() {
    fetch(`${location.origin}/api/${this.$route.params.gid}/details`)
      .then(resp => resp.json())
      .then(data => {
        this.details = data
      });
    //fetch(`${location.origin}/api/${this.$route.params.gid}/prices`)
    //    .then(resp => resp.json())
    //    .then(data => {
    //      this.prices = data.prices
    //    });
  }
}
</script>

<style scoped>

</style>