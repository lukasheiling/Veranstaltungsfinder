<template>
  <div id="app">
    <h1>Events</h1>
    <ul>
      <li v-for="event in events" :key="event.id">
        {{ event.name }} - {{ event.date }} - {{ event.venue }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      events: [],
    };
  },
  async created() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/events/');
      this.events = response.data;
    } catch (error) {
      console.error(error);
    }
  },
};
</script>

<style>
/* Deine Styles hier */
</style>
