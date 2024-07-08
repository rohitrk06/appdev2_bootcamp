<script setup>
import {ref } from 'vue';
import {useRouter} from 'vue-router';
import {messageStore} from '@/stores/messageStore';
import {auth} from '@/stores/auth'; 

const message_store = messageStore();
const auth_store = auth();

const router = useRouter();
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

fetchCategories();

const product_name = ref('');
const description = ref('');
const cost_price = ref(0);
const selling_price = ref(0);
const categorySelected = ref('');
const mfg_date = ref('');
const expiry_date = ref('');
const stock = ref(0);

function validate_input(){
    if (cost_price.value < 0){
        message_store.setmessage('Cost Price should be greater than 0')
        return false
    }
    if (selling_price.value < 0){
        message_store.setmessage('Selling Price should be greater than 0')
        return false
    }
    if (selling_price.value < cost_price.value){
        message_store.setmessage('Selling Price should be greater than Cost Price')
        return false
    }
    if (stock.value < 0){
        message_store.setmessage('Stock should be greater than 0')
        return false
    }
    return true
}

function addProduct(){
    const product_details = {
        'name': product_name.value,
        'description': description.value,
        'cost_price': cost_price.value,
        'selling_price': selling_price.value,
        'category_name': categorySelected.value,
        'manufacture_date': mfg_date.value,
        'expiry_date': expiry_date.value,
        'stock': stock.value
    }
    if (validate_input()){
        try{
            // console.log(auth_store.token)
            fetch(`${auth_store.backend_url}/api/v1/product`, {
                method: 'POST',
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
                                message: 'Error Adding Product'
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
    <h1 class="text-center">Add Product</h1>
    <div class="d-flex justify-content-center">
        <form class="w-50 justify-content-center" @submit.prevent="addProduct">
            <div class="mb-3">
                <label for="product_name" class="form-label"><strong>Product Name</strong></label>
                <input type="text" class="form-control" id="product_name" v-model = 'product_name'>
            </div>
            <div class="mb-3">
                <label for="description" class="form-label"><strong>Product Description</strong></label>
                <textarea class="form-control" id="description" v-model = description></textarea>
            </div>
            <div class="row">
                <div class="mb-3 col-6">
                    <label for="cost_price" class="form-label"><strong>Cost Price</strong></label>
                    <input type="number" class="form-control" id="cost_price" v-model = 'cost_price' required>
                </div>
                <div class="mb-3 col-6">
                    <label for="selling_price" class="form-label"><strong>Selling Price</strong> </label>
                    <input type="number" class="form-control" id="selling_price" v-model = 'selling_price'>
                </div>
            </div>
            <div class="mb-3">
                <label for="category" class="form-label">Category</label>
                <select class="form-select" id="category" v-model="categorySelected">
                    <option v-for="category in categories" :value="category.name" >{{ category.name }}</option>
                </select>
            </div>
            <div class="row">
                <div class="mb-3 col-4">
                    <label for="manufacturing_date" class="form-label"><strong>Manufacture Date</strong></label>
                    <input type="date" class="form-control" id="manufacturing_date" v-model = 'mfg_date' required>
                </div>
                <div class="mb-3 col-4">
                    <label for="expiry_date" class="form-label"><strong>Expiry Date</strong> </label>
                    <input type="date" class="form-control" id="expiry_date" v-model = 'expiry_date'>
                </div>
                <div class="mb-3 col-4">
                    <label for="stock" class="form-label"><strong>Available Stock</strong></label>
                    <input type="number" class="form-control" id="stock" v-model = 'stock' required> 
                </div>
            </div>
            <div class="d-flex justify-content-center mb-3">
                <button type="submit" class="btn btn-primary">Add</button>
            </div>
        </form> 
    </div>
</div>
</template>