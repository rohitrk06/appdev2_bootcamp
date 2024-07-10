<template>
<div class="container-fluid mt-2 p-3">
    <h1 class="text-center">Edit Category</h1>
    <div class="d-flex justify-content-center">
        <form class="w-50 justify-content-center" @submit.prevent="editCategory">
            <div class="mb-3">
                <label for="category_name" class="form-label">Category Name</label>
                <input type="test" class="form-control" id="category_name" v-model = category.name>
            </div>
            <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea class="form-control" id="description" v-model = 'category.description'></textarea>
            </div>
            <div class="d-flex justify-content-center mb-3">
                <button type="submit" class="btn btn-primary">Edit</button>
            </div>
        </form>
    </div>  
</div>
</template>

<script setup>
import {useRoute} from 'vue-router';
import {auth} from '@/stores/auth';
import {messageStore} from '@/stores/messageStore';
import {onMounted} from 'vue';
import {computed} from 'vue';
import {useRouter} from 'vue-router';
import { ref } from 'vue';

const auth_store = auth();
const message_store = messageStore();
const route = useRoute();  
const router = useRouter();
const category_id = route.params.id;
// console.log(category_id);
const category = ref({
    name: '',
    description: ''
});

onMounted(()=>{
    getCategory();
})

function getCategory(){
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
                    category.value.name = data.name;
                    category.value.description = data.description;
                }
            )
    }
    catch(error){
        console.log(error);
    }
}


function validate_input(){
    if (category.value.category_name == ''){
        message_store.setmessage('Category Name is required');
        return false;
    }
    return true;
}

function editCategory(){
    if (validate_input()){
        try{
            fetch(`${auth_store.backend_url}/api/v1/category/${category_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Authentication-Token': auth_store.token
                    },
                body: JSON.stringify(category.value)
                }).then(
                    (response) =>{
                        return response.json();
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