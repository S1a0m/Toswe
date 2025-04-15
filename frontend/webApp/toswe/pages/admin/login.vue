<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCookie } from '#app' // pour manipuler les cookies

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const router = useRouter()

async function handleLogin() {
  try {
    const response = await $fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      body: {
        mobile_number: email.value, // remplace par email si besoin
        password: password.value
      }
    })

    const { access_token, refresh_token } = response

    // Stockage des tokens dans localStorage ou cookie (selon ton choix de sécurité)
    localStorage.setItem('access_token', access_token)
    localStorage.setItem('refresh_token', refresh_token)

    // OU : avec cookies pour sécurité + SSR friendly
    // useCookie('access_token').value = access_token
    // useCookie('refresh_token').value = refresh_token

    // Redirection après succès
    router.push('/admin/products')
  } catch (err) {
    console.error(err)
    errorMessage.value = err?.data?.detail || 'Erreur lors de la connexion'
  }
}

definePageMeta({
  layout: 'admin'
})
</script>


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
  