<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" autocomplete="email">
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" autocomplete="current-password">
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
        const response = await axios.post('http://127.0.0.1:8000/token', {
          email: this.email,  // Verwende hier 'email' anstelle von 'username'
          password: this.password
        });
        console.log('Login Success:', response.data);
        localStorage.setItem('user', JSON.stringify(response.data));
        this.$emit('login-success');
      } catch (error) {
        console.error('Login error:', error.response ? error.response.data : 'Unknown error');
        alert('Failed to login. ' + (error.response ? JSON.stringify(error.response.data.detail) : 'No response from server'));
      }
    }
  }
};
</script>
