<template>
  <v-form>
    <v-container fluid>
      <v-row class="content" align="center" justify="center">
        <v-col cols="8">
          <v-row>
            <v-col cols="12">
              <v-text-field v-model="search" label="Search"></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="3" offset="3">
              <v-btn color="secondary" block="true">
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
.content {
  height: calc(100vh - 88px)
}
</style>

<script>
export default {
  data: () => ({
    search: '',
  }),
  methods: {
    submit(){
      this.$router.push({path: "/search", query: {q: this.search}})
    }
  },
  mounted() {
    let qparams = this.$route.query
    if (qparams.q) {
      this.search = qparams.q
    }
  }
}
</script>