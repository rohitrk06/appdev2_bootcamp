<script setup>
import { auth } from '@/stores/auth';
import { messageStore } from '@/stores/messageStore';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const message_store = messageStore();
const auth_store = auth();

auth_store.logout().then(
    (resp)=>{
        message_store.setmessage(resp.message)
        if (resp.status){
            router.push({path: '/'})
        }
    }
)

</script>
