<template>
    <div class="auth-container">
      <h1>Register</h1>
      <form @submit.prevent="register" class="auth-form">
        <div class="input-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" autocomplete="email">
        </div>
        <div class="input-group">
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
          this.$emit('register-success');
        } catch (error) {
          console.error('Registration error:', error.response ? error.response.data : 'Unknown error');
          alert('Failed to register. ' + (error.response ? error.response.data.detail : 'No response from server'));
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .auth-container {
    max-width: 300px;
    margin: auto;
    padding: 20px;
    background: #f4f4f9;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  }
  
  .auth-form {
    display: flex;
    flex-direction: column;
  }
  
  .input-group {
    margin-bottom: 15px;
  }
  
  input[type="email"], input[type="password"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    padding: 10px;
    background-color: #5C67F2;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #5058e5;
  }
  </style>
  