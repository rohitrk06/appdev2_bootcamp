import { ref, computed } from 'vue'
import { defineStore } from 'pinia'


export const auth = defineStore('auth',()=>{
    const backend_url = 'http://127.0.0.1:5000'
    const token = ref(computed(()=>localStorage.getItem('token')))
    const username = ref(computed(()=>localStorage.getItem('username')))

    const isAuthenticated = computed(()=>token.value !== null)
    
    async function login(user_details){
        console.log(user_details)
        try{
            const response = await fetch(`${backend_url}/api/v1/login`,{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                body: JSON.stringify(user_details)
            })
            console.log(await response.json())
        }
        catch(error){
            console.error(error)
        }
        return true
    }

    return {login, token, username, isAuthenticated}
});
