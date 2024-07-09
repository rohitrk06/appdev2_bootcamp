<script setup>
import { defineProps, ref } from 'vue';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { onMounted } from 'vue';
import Product from '@/components/Product.vue';

const auth_store = auth();
const message_store = messageStore()
const category = defineProps(['category_id']);
const category_data = ref({
    category_id: 0,
    category_name: '',
    category_description: '',
    products: []
});

// const category_products = ref({
//     'products': []
// });

onMounted(()=>{
    getCategory(category.category_id);
    getProducts(category.category_id);
})

function getProducts(category_id) {
    try{
        fetch(`${auth_store.backend_url}/api/v1/${category_id}/products`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                },
            }).then(
                (response) =>{
                    return response.json();
                }
            ).then(
                (data)=>{
                    console.log(data);
                    category_data.value.products = data;
                    console.log('From categories component');
                    console.log(category_data.value.products);
                }
            )
    }
    catch(error){
        console.log(error);
    }
}

function getCategory(category_id) {
    try{
        fetch(`${auth_store.backend_url}/api/v1/category/${category_id}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                },
            }).then(
                (response) =>{
                    return response.json();
                }
            ).then(
                (data)=>{
                    console.log(data);
                    category_data.value.category_id = data.category_id;
                    category_data.value.category_name = data.name;
                    category_data.value.category_description = data.description;

                    // category_name = data.name
                }
            )
    }
    catch(error){
        console.log(error);
    }
}

</script>

<template>
<div class="container-fluid mt-1 p-2">
    <p class="h1">{{category_data.category_name}}</p>
    <hr>
    <div class="row">
        <Product v-for="product in category_data.products" :product_details="product" :key="product.id"/>
        <!-- <Product v-for="product in category_data.products" :product_details="product" :key="product.id"/> -->
    </div>  
</div>
</template>