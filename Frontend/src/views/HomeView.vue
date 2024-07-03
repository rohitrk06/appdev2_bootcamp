<script setup>
import { RouterLink } from 'vue-router';
import TheWelcome from '../components/TheWelcome.vue'

import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Categories from '../components/Categories.vue';

const auth_store = auth();


</script>

<template>
<div v-if="auth_store.isAuthenticated">
  <!-- <div v-for="" -->
  <Categories :category_id="1"/>

</div>
<div class="container-fluid mt-5 p-5" v-if="!auth_store.isAuthenticated">
    <h1 class="text-center">Welcome to Grocery Store</h1>
    <p class="text-center">Buy groceries online from the comfort of your home.</p>
    <div class="d-flex justify-content-center">
      <RouterLink class="btn btn-primary justify-content-center" to="/login" >Shop Now </RouterLink>
    </div>  
</div>
</template>
