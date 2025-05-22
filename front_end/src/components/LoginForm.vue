<template>
  <div class="login-form">
    <h2>로그인</h2>
    <input v-model="username" placeholder="아이디" />
    <input v-model="password" type="password" placeholder="비밀번호" />
    <div class="btn-group">
      <button @click="login">로그인</button>
      <button @click="register">회원가입</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
  try {
    const res = await axios.post('http://localhost:8000/api/login', {
      username: username.value,
      password: password.value,
    })
    alert('로그인 성공')
    // 토큰 저장 등 추가 처리 가능
  } catch (e) {
    alert('로그인 실패')
  }
}

const register = async () => {
  router.push('/signup')
}
</script>

<style scoped>
.login-form {
  width: 100%;
  max-width: 600px;
  margin: 4rem auto;
  padding: 4rem 5rem;
  border-radius: 32px;
  background: #fff;
  box-shadow: 0 8px 40px #007bff11, 0 2px 16px #0002;
  display: flex;
  flex-direction: column;
  gap: 1.7rem;
  box-sizing: border-box;
}

h2 {
  font-size: 2rem;
  text-align: center;
  color: #007bff;
  font-weight: 700;
  margin-bottom: 1.5rem;
}

input {
  width: 100%;
  font-size: 1.2rem;
  padding: 1.2rem 1.5rem;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  background: #fafbfc;
  transition: border 0.2s;
}

input:focus {
  border-color: #007bff;
  background: #fff;
  outline: none;
}

.btn-group {
  display: flex;
  gap: 1rem;
}

button {
  flex: 1;
  font-size: 1.2rem;
  padding: 1rem 0;
  border: none;
  border-radius: 12px;
  background: linear-gradient(90deg, #7ecbff 0%, #007bff 100%);
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 18px #007bff22;
  transition: background 0.2s;
}

button:hover {
  background: linear-gradient(90deg, #4fa3e3 0%, #0056b3 100%);
}

</style> 