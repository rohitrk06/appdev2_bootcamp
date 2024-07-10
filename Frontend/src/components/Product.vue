<script setup>
import { defineProps, ref } from 'vue';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { onMounted } from 'vue';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const auth_store = auth();
const message_store = messageStore()
const router = useRouter();
const product = defineProps(['product_details']);
const update_url = computed(() => {
    return `/update_product/${product.product_details.product_id}`
})
const delete_url = computed(() => {
    return `/delete_product/${product.product_details.product_id}`
})

</script>

<template>
<div class="card col-3 m-1">
            <div class="card-body">
              <h5 class="card-title">{{product.product_details.name}}</h5>
              <p class="card-text"><em>{{product.product_details.description}}</em></p>
              <div class="row">
                <div class="col-6">
                    <p class="card-text"><strong>Mfg Date:</strong> {{product.product_details.manufacture_date}}</p>
                </div>
                <div class="col-6">
                    <p class="card-text"><strong>Expriy Date:</strong> {{product.product_details.expiry_date}}</p>
                </div>
              </div>
              <div class="row">
                <div class="col-6">
                    <p class="card-text mt-4"><strong>Price:</strong> {{product.product_details.selling_price}}</p>
                </div>
              </div>
                <div class="row mt-3 container-fluid justify-content-center" v-if="auth_store.isAuthenticated && auth_store.role==='manager'">
                    <div class="col-6">
                        <RouterLink class="btn btn-primary" :to="update_url" >Update</RouterLink>
                    </div>
                    <div class="col-6">
                        <RouterLink class="btn btn-primary" :to="delete_url">Delete</RouterLink>
                    </div>
                </div>
                <div class="contain-fluid mt-3" v-if="auth_store.isAuthenticated && auth_store.role === 'user'">
                    <form method="POST">
                        <div class="row d-flex justify-content-center">
                        <div class="col-6">
                            <label for="quantity" class="form-label">Quantity</label>
                            <input type="number" name="quantity" class="form-control" placeholder="Quantity">
                        </div>
                        <div class="col-4">
                            <button type="submit" class="btn btn-primary">Add to Cart</button>
                        </div>
                    </div>
                    </form>
                </div>
            </div>
        </div>
</template>