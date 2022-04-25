<template>
  <v-form>
    <v-container fluid style="min-height: calc(100vh - 80px)">
      <v-row style="min-height: 80vh" align="center" justify="center">
        <v-col cols="8">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="search" label="Search"></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-expand-transition>
                <div v-if="isAdvSearch">
                  <v-row>
                    <v-col>
                      Advanced Search
                      <v-divider></v-divider>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col cols="4">
                      <v-autocomplete
                          v-model="sGenres"
                          v-model:search="vGenre"
                          :items="genres"
                          :loading="genres.length === 0"
                          label="Genres"
                          chips closable-chips small-chips multiple>
                      </v-autocomplete>
                    </v-col>
                    <v-col cols="4">
                      <v-autocomplete
                          v-model="sDev"
                          v-model:search="vDev"
                          :items="devs"
                          :loading="devsLoading"
                          label="Developer"
                          filled clearable>
                      </v-autocomplete>
                    </v-col>
                    <v-col cols="4">
                      <v-autocomplete
                          v-model="sPub"
                          v-model:search="vPub"
                          :items="pubs"
                          :loading="pubsLoading"
                          label="Publisher"
                          filled clearable>
                      </v-autocomplete>
                    </v-col>
                  </v-row>
                </div>
              </v-expand-transition>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="3" offset="3">
              <v-btn color="secondary" block="true" @click="isAdvSearch = !isAdvSearch">
                Advanced Search
              </v-btn>
            </v-col>
            <v-col cols="3">
              <v-btn color="primary" block="true" type="submit" :disabled="!search" @click.stop.prevent="submit()">
                Submit
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<style scoped>
</style>

<script>
export default {
  data: () => ({
    search: '',
    isAdvSearch: false,
    genres: [],
    genresLoading: false,
    pubs: [],
    pubsLoading: false,
    devs: [],
    devsLoading: false,
    sGenres: [],
    sDev: null,
    sPub: null,
    vGenre: "",
    vDev: "",
    vPub: "",
  }),
  watch: {
    vDev(val) {
      if (val.length < 3) return

      this.devsLoading = true
      fetch(`${location.origin}/api/dev/${val}`)
          .then(resp => resp.json())
          .then(data => {
            this.devs = data.devs
          })
          .finally(() => (this.devsLoading = false));

    },
    vPub(val) {
      if (val.length < 3) return

      this.pubsLoading = true
      fetch(`${location.origin}/api/pub/${val}`)
          .then(resp => resp.json())
          .then(data => {
            this.pubs = data.pubs
          })
          .finally(() => (this.pubsLoading = false));
    },
  },
  methods: {
    submit() {
      let q = {q: this.search}
      if (this.isAdvSearch) {
        q.isAdvSearch = true
        if (this.sGenres.length !== 0) {
          q.genres = this.sGenres.join()
        }
        if (this.sDev) {
          q.dev = this.sDev
        }
        if (this.sPub) {
          q.pub = this.sPub
        }
      }
      this.$router.push({path: "/search", query: q})
    }
  },
  mounted() {
    let qparams = this.$route.query
    if (qparams.q) {
      this.search = qparams.q
    }
    if (qparams.isAdvSearch) {
      this.isAdvSearch = true
    }
    if (qparams.genres) {
      this.sGenres = qparams.genres.split(",")
    }
    if (qparams.dev) {
      this.sDev = qparams.dev
    }
    if (qparams.pub) {
      this.sPub = qparams.pub
    }
    fetch(`${location.origin}/api/genres`)
        .then(resp => resp.json())
        .then(data => {
          this.genres = data.genres
        });
  }
}
</script>