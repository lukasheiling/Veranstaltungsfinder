<template>
    <div>
      <h1>Login</h1>
      <form @submit.prevent="login">
        <div>
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email">
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password">
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        email: '',
        password: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post('http://127.0.0.1:8000/login/', {
            email: this.email,
            password: this.password
          });
          console.log('Success:', response.data);
          // Speichern des Tokens oder anderer Auth-Daten, z.B. im localStorage
          localStorage.setItem('user', JSON.stringify(response.data));
          this.$router.push('/home'); // Umleitung auf die Startseite oder Dashboard
        } catch (error) {
          console.error('Login error:', error.response.data);
          alert('Failed to login');
        }
      }
    }
  };
  </script>
  