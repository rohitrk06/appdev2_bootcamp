<script setup>
import { defineProps, ref } from 'vue';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { onMounted } from 'vue';
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import { useRouter } from 'vue-router';

const route = useRoute();
const product_id = route.params.id;
const auth_store = auth();
const message_store = messageStore();
const router = useRouter();
onMounted(()=>{
    fetchProduct();
    fetchCategories();
})

const categorySelected= ref('');
const product = ref({});
const categories = ref([]);
function fetchCategories(){
    try{
        fetch(`${auth_store.backend_url}/api/v1/get_all_categories`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                },
            }).then(
                (response) =>{
                    if (!response.ok){
                        const resp = {
                            status: false,
                            message: 'Error Fetching Categories'
                        }
                        return resp
                    }
                    else{
                        return response.json();
                    }
                }
            ).then(
                (data)=>{
                    if (data.status == false){
                        message_store.setmessage(data.message)
                    }
                    else{
                        categories.value = data;
                    }
                }
            )
    }
    catch(error){
        console.log(error);
    }
}

function fetchProduct(){
    try{
        fetch(`${auth_store.backend_url}/api/v1/product/${product_id}`, {
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
                    product.value = data;
                    categorySelected.value = data.category.name;
                }
            )
    }
    catch(error){
        console.log(error);
    }
}

function validate_input(){
    if (product.value.cost_price < 0){
        message_store.setmessage('Cost Price should be greater than 0')
        return false
    }
    if (product.value.selling_price < 0){
        message_store.setmessage('Selling Price should be greater than 0')
        return false
    }
    if (product.value.selling_price < product.value.cost_price){
        message_store.setmessage('Selling Price should be greater than Cost Price')
        return false
    }
    if (product.value.stock < 0){
        message_store.setmessage('Stock should be greater than 0')
        return false
    }
    return true
}

function editProduct(){
    const product_details = {
        'name': product.value.name,
        'description': product.value.description,
        'cost_price': product.value.cost_price,
        'selling_price': product.value.selling_price,
        'category': categorySelected.value,
        'manufacture_date': product.value.manufacture_date,
        'expiry_date': product.value.expiry_date,
        'stock': product.value.stock
    }
    if (validate_input()){
        try{
            // console.log(auth_store.token)
            fetch(`${auth_store.backend_url}/api/v1/product/${product_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Authentication-Token': auth_store.token
                    },
                body: JSON.stringify(product_details)
                }).then(
                    (response) =>{
                        if (!response.ok){
                            const resp = {
                                status: false,
                                message: 'Error updating Product'
                            }
                            return resp
                        }
                        else{
                            return response.json();
                        }
                    }
                ).then(
                    (data)=>{
                        message_store.setmessage(data.message)
                        router.push('/')
                    }
                )
        }
        catch(error){
            console.log(error);
        }

    }
}


</script>

<template>
<div class="container-fluid mt-2 p-3">
    <h1 class="text-center">Edit Product Details</h1>
    <div class="d-flex justify-content-center">
        <form class="w-50 justify-content-center" @submit.prevent="editProduct">
            <div class="mb-3">
                <label for="product_name" class="form-label"><strong>Product Name</strong></label>
                <input type="text" class="form-control" id="product_name" v-model = "product.name">
            </div>
            <div class="mb-3">
                <label for="description" class="form-label"><strong>Product Description</strong></label>
                <textarea class="form-control" id="description" v-model = 'product.description' ></textarea>
            </div>
            <div class="row">
                <div class="mb-3 col-6">
                    <label for="cost_price" class="form-label"><strong>Cost Price</strong></label>
                    <input type="number" class="form-control" id="cost_price" v-model="product.cost_price" required>
                </div>
                <div class="mb-3 col-6">
                    <label for="selling_price" class="form-label"><strong>Selling Price</strong> </label>
                    <input type="number" class="form-control" id="selling_price" v-model="product.selling_price">
                </div>
            </div>
            <div class="mb-3">
                <label for="category" class="form-label">Category</label>
                <select class="form-select" id="category" v-model="categorySelected">
                    <option v-for="category in categories" :value="category.name">{{ category.name }}</option>
                </select>
            </div>
            <div class="row">
                <div class="mb-3 col-4">
                    <label for="manufacturing_date" class="form-label"><strong>Manufacture Date</strong></label>
                    <input type="date" class="form-control" id="manufacturing_date" v-model="product.manufacture_date" required>
                </div>
                <div class="mb-3 col-4">
                    <label for="expiry_date" class="form-label"><strong>Expiry Date</strong> </label>
                    <input type="date" class="form-control" id="expiry_date" v-model = "product.expiry_date">
                </div>
                <div class="mb-3 col-4">
                    <label for="stock" class="form-label"><strong>Available Stock</strong></label>
                    <input type="number" class="form-control" id="stock" v-model="product.stock" required> 
                </div>
            </div>
            <div class="d-flex justify-content-center mb-3">
                <button type="submit" class="btn btn-primary">Edit Product</button>
            </div>
        </form> 
    </div>
</div>

</template>