<template>
  <div id="app">
    <div v-if="!isLoggedIn">
      <button @click="showRegisterForm = false">Login</button>
      <button @click="showRegisterForm = true">Register</button>
      <user-login v-if="!showRegisterForm" @login-success="handleLoginSuccess"></user-login>
      <user-register v-else @register-success="handleRegisterSuccess"></user-register>
    </div>
    <div v-else>
      <h1>Eventfinder</h1>
      <button @click="logout">Logout</button>
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
  </div>
</template>

<script>
import axios from 'axios';
import UserLogin from './components/UserLogin.vue';
import UserRegister from './components/UserRegister.vue';

export default {
  name: 'App',
  components: {
    UserLogin,
    UserRegister
  },
  data() {
    return {
      isLoggedIn: !!localStorage.getItem('user'),
      showRegisterForm: false,
      events: [],
      country: ''
    };
  },
  methods: {
    handleLoginSuccess() {
      this.isLoggedIn = true;
      this.showRegisterForm = false;
    },
    handleRegisterSuccess() {
      this.isLoggedIn = true; // Optional: Log in the user automatically after registration
      this.showRegisterForm = false;
    },
    logout() {
      localStorage.removeItem('user');
      this.isLoggedIn = false;
    },
    fetchEvents() {
      if (!this.country) {
        alert('Please enter a country code.');
        return;
      }
      axios.get(`http://127.0.0.1:8000/events/`, { params: { country: this.country } })
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
  margin: 20px; /* Uniform margin on all sides */
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

button {
  margin: 10px 0; /* Abstand oben und unten für Buttons */
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
