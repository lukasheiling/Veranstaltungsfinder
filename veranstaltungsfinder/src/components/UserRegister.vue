<template>
    <div>
      <h1>Register</h1>
      <form @submit.prevent="register">
        <div>
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" autocomplete="email">
        </div>
        <div>
          <label for="password">Password:</label>
          <input type="password" id="password" v-model="password" autocomplete="new-password">
        </div>
        <button type="submit">Register</button>
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
        async register() {
            try {
                const response = await axios.post('http://127.0.0.1:8000/users/', {
                email: this.email,
                password: this.password
                });
                console.log('Registration Success:', response.data);
                // Optional: Auto-login after registration or redirect to login
                this.$emit('register-success'); // Emit an event to notify the parent component
                this.$router.push('/'); // Redirect to home or dashboard
            } catch (error) {
                console.error('Registration error:', error.response ? error.response.data : 'Unknown error');
                alert('Failed to register. ' + (error.response ? error.response.data.detail : 'No response from server'));
            }
        }

    }
  };
  </script>
  