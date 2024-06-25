<script setup>
import { RouterLink } from 'vue-router';
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
<div class="container-fluid mt-5 p-5">
    <h1 class="text-center">Welcome to Grocery Store</h1>
    <p class="text-center">Buy groceries online from the comfort of your home.</p>
    <div class="d-flex justify-content-center">
      <RouterLink class="btn btn-primary justify-content-center" to="/login" >Shop Now </RouterLink>
    </div>  
</div>
</template>
