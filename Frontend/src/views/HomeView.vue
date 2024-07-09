<script setup>
import { RouterLink } from 'vue-router';
import TheWelcome from '../components/TheWelcome.vue'

import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Categories from '../components/Categories.vue';
import { onMounted } from 'vue';

const auth_store = auth();
const all_categories = ref([]);
onMounted(()=>{
  fetch_categories();
})

function fetch_categories(){
  try{
    fetch(`${auth_store.backend_url}/api/v1/get_all_categories`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    }).then(
      (response) => {
        if (!response.ok){
          const data =  response.json()
          const rsp = {
              'status': false,
              'message': data.message
          }
          return rsp
        }
        else {
          return response.json()
        }
      }
    ).then(
      (data) => {
        if (data.status === false){
          messageStore.addMessage(data.message, 'danger')
          return
        }
        all_categories.value = data;
        console.log('From Home component');
        console.log(all_categories.value);
      }
    )
  }
  catch(error){
    console.log(error);
  }
}


</script>

<template>
<div v-if="auth_store.isAuthenticated">
  <!-- <div v-for="" -->
  <Categories v-for="category in all_categories" :category_id="category.category_id"/>

</div>
<div class="container-fluid mt-5 p-5" v-if="!auth_store.isAuthenticated">
    <h1 class="text-center">Welcome to Grocery Store</h1>
    <p class="text-center">Buy groceries online from the comfort of your home.</p>
    <div class="d-flex justify-content-center">
      <RouterLink class="btn btn-primary justify-content-center" to="/login" >Shop Now </RouterLink>
    </div>  
</div>
</template>
