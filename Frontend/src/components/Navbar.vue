<script setup>
import { RouterLink} from 'vue-router';
import { auth } from '@/stores/auth';

const auth_store = auth();


</script>

<template>
    <nav class="navbar bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand h1 m-0" href="#">Grocery Store</a>
        
            <form class="d-flex" role="search">
                <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
                <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
    
            <ul class="nav justify-content-end ">
                <li class="nav-item" v-if="!auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/login">Login</RouterLink>
                </li>
                <li class="nav-item" v-if="!auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/register">Register</RouterLink>
                </li>
                <li class="nav-item" v-if="auth_store.isAuthenticated">
                    <RouterLink class="nav-link" to="/logout">Logout</RouterLink>
                </li>
                <li class="nav-item disabled" v-if="auth_store.isAuthenticated">
                    <a class="nav-link">{{auth_store.username}}</a>
                </li>
            </ul>

            
        </div>
    </nav>
</template>