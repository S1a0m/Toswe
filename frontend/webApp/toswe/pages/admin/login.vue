<template>
    <div class="admin-login">
      <div class="login-box">
        <h1>Connexion Admin</h1>
        <form @submit.prevent="handleLogin">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="email" required />
  
          <label for="password">Mot de passe</label>
          <input type="password" id="password" v-model="password" required />
  
          <div class="actions">
            <button type="submit">Se connecter</button>
            <button type="button" class="cancel" @click="reset">Annuler</button>
          </div>
  
          <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const email = ref('')
  const password = ref('')
  const errorMessage = ref('')
  
  function handleLogin() {
    if (email.value === 'admin@example.com' && password.value === 'admin123') {
      console.log('Connexion réussie')
      // Rediriger ou stocker l'état de connexion ici
    } else {
      errorMessage.value = 'Identifiants incorrects'
    }
  }
  
  function reset() {
    email.value = ''
    password.value = ''
    errorMessage.value = ''
  }

  definePageMeta({
  layout: 'admin'
})
  </script>
  
  <style scoped lang="scss">
  .admin-login {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    // background: linear-gradient(to bottom right, #f5e6da, #d5c5b0);
  
    .login-box {
      background: rgba(245, 230, 218, 0.7);
      padding: 40px;
      border-radius: 20px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
      width: 400px;
      text-align: center;
  
      h1 {
        margin-bottom: 30px;
        color: #c0a080;
        font-size: 28px;
      }
  
      label {
        display: block;
        text-align: left;
        font-weight: bold;
        margin-top: 15px;
        margin-bottom: 5px;
      }
  
      input {
        width: 100%;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 10px;
        margin-bottom: 10px;
        font-size: 16px;
        transition: 0.2s;
  
        &:focus {
          outline: none;
          border-color: #c0a080;
          box-shadow: 0 0 5px #c0a08055;
        }
      }
  
      .actions {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
  
        button {
          padding: 10px 20px;
          border-radius: 10px;
          border: none;
          font-weight: bold;
          font-size: 16px;
          cursor: pointer;
          transition: 0.2s;
  
          &:first-of-type {
            background-color: #c0a080;
            color: white;
  
            &:hover {
              background-color: #a08060;
            }
          }
  
          &.cancel {
            background-color: #f0f0f0;
  
            &:hover {
              background-color: #e0e0e0;
            }
          }
        }
      }
  
      .error {
        color: red;
        margin-top: 15px;
        font-weight: bold;
      }
    }
  }
  </style>
  