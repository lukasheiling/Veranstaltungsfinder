<template>
  <div id="app">
    <h1>Eventfinder</h1>
    <div>
      <label for="country">Country:</label>
      <input type="text" id="country" v-model="country" placeholder="Enter country code (e.g., US, DE)">
    </div>
    <button @click="fetchEvents">Load Events</button>
    <ul>
      <li v-for="event in events" :key="event.id">
        <div class="event-name">{{ event.name }}</div>
        <div class="event-details">
          <span>{{ event.date }}</span> - <span>{{ event.venue }}</span>
        </div>
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
      country: '',  // Stelle sicher, dass diese Variable mit dem Input-Feld gebunden ist
    };
  },
  methods: {
  fetchEvents() {
    const country = this.country; // Stellen Sie sicher, dass `this.country` korrekt gesetzt ist
      if (!country) {
        alert('Please enter a country code.');
        return;
      }
      axios.get(`http://127.0.0.1:8000/events/`, { params: { country } })
        .then(response => {
          this.events = response.data;
        })
        .catch(error => {
          console.error("Error fetching events:", error);
          alert(`Failed to fetch events: ${error.message}`);
        });
    }
  }
};
</script>

<style scoped>
#app {
  font-family: 'Arial', sans-serif;
  width: 100%; /* Nutze die volle Breite für eine responsive Ansicht */
  max-width: 800px; /* Maximale Breite bleibt, aber nur für Inhalte relevant */
  margin: 20px 20px 20px 20px; /* Oben, Rechts, Unten, Links */
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  border-radius: 8px;
  background: #fff;
  align-items: flex-start; /* Inhalte linksbündig ausrichten */
}

h1 {
  color: #2C3E50;
  text-align: left; /* Überschrift auch linksbündig */
  margin-bottom: 20px;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

li {
  padding: 10px;
  margin-bottom: 10px;
  border-bottom: 1px solid #ecf0f1;
  transition: background-color 0.3s;
}

li:hover {
  background-color: #ecf0f1;
}

li:last-child {
  border-bottom: none;
}

.event-name {
  font-size: 1.2em;
  font-weight: bold;
}

.event-details {
  font-size: 0.9em;
  color: #7f8c8d;
}
</style>
