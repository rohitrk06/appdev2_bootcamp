<script setup>
import { defineProps, ref } from 'vue';
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { onMounted } from 'vue';
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import {useRoute } from 'vue-router';

const auth_store = auth();
const message_store = messageStore()
const router = useRouter();
const route = useRoute();

const product_id = route.params.id;

onMounted(()=>{
    deleteProduct();
})


function deleteProduct(){
    try{
        fetch(`${auth_store.backend_url}/api/v1/product/${product_id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Authentication-Token':auth_store.token
            },
        }).then(
            (response) =>{
                return response.json();
            }
        ).then(
            (data)=>{
                message_store.setmessage(data.message);
                router.push('/')
            }
        )
    }
    catch(error){
        console.log(error);
    
    }
}


</script>

<!-- <template>

</template> -->