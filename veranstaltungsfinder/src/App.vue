<template>
  <div id="app">
    <div v-if="!isLoggedIn">
      <div class="auth-buttons">
        <button @click="showRegisterForm = false">Login</button>
        <button @click="showRegisterForm = true">Register</button>
      </div>
      <user-login v-if="!showRegisterForm" @login-success="handleLoginSuccess"></user-login>
      <user-register v-else @register-success="handleRegisterSuccess"></user-register>
    </div>
    <div v-else>
      <header class="header">
        <h1>Eventfinder</h1>
        <button class="logout-button" @click="logout">Logout</button>
      </header>
      <div class="search-bar">
        <label for="country">Country:</label>
        <input type="text" id="country" v-model="country" placeholder="Enter country code (e.g., US, DE)">
        <button @click="fetchEvents">Load Events</button>
      </div>
      <ul class="event-list">
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
  font-family: 'Lato', sans-serif;
  width: 100%;
  max-width: 960px;
  margin: 20px auto;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  border-radius: 8px;
  background: #fff;
}

.auth-buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 1px solid #ccc;
}

.logout-button {
  padding: 8px 16px;
  background-color: #d32f2f;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}

h1 {
  color: #333;
  margin: 0;
}

button {
  cursor: pointer;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  margin-left: 10px;
}

.search-bar {
  margin-top: 20px;
  display: flex;
  align-items: center;
}

.event-list {
  list-style: none;
  margin: 20px 0;
  padding: 0;
}

li {
  padding: 10px;
  margin-bottom: 10px;
  border-bottom: 1px solid #ccc;
}

.event-name {
  font-size: 1.2em;
  font-weight: bold;
}

.event-details {
  font-size: 0.9em;
  color: #666;
}

input[type="text"] {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 250px;
}

label {
  margin-right: 10px;
}

@media (max-width: 600px) {
  .header, .search-bar {
    flex-direction: column;
    align-items: flex-start;
  }

  .logout-button {
    margin-top: 10px;
  }

  .search-bar {
    width: 100%;
  }

  input[type="text"] {
    width: calc(100% - 20px); /* Adjust based on padding */
  }

  button {
    width: 100%;
    margin-top: 10px;
  }
}
</style>