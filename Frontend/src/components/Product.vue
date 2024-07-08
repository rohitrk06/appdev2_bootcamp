<script setup>
import { defineProps, ref } from 'vue';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { onMounted } from 'vue';

const auth_store = auth();
const message_store = messageStore()

const product = defineProps(['product']);

console.log(product);

</script>

<template>
<div class="card col-3 m-1">
            <div class="card-body">
              <h5 class="card-title">{{product.name}}</h5>
              <p class="card-text"><em>{{product.description}}</em></p>
              <div class="row">
                <div class="col-6">
                    <p class="card-text"><strong>Mfg Date:</strong> {{product.manufacture_date}}</p>
                </div>
                <div class="col-6">
                    <p class="card-text"><strong>Expriy Date:</strong> {{product.expiry_date}}</p>
                </div>
              </div>
              <div class="row">
                <div class="col-6">
                    <p class="card-text mt-4"><strong>Price:</strong> {{product.selling_price}}</p>
                </div>
              </div>
                <div class="row mt-3 container-fluid justify-content-center" v-if="auth_store.isAuthenticated && auth_store.role==='manager'">
                    <div class="col-6">
                        <button class="btn btn-primary">Update</button>
                    </div>
                    <div class="col-6">
                        <button class="btn btn-primary">Delete</button>
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