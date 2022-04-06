<template>
  <v-app>
    <v-app-bar>
      <v-app-bar-title>Steam Games Search Engine</v-app-bar-title>

    </v-app-bar>
    <v-main>
        <router-view></router-view>
    </v-main>
    <v-footer app>
    </v-footer>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  components: {
  },

  data: () => ({
  })
}
</script>
