import { ref, computed } from 'vue'
import { defineStore } from 'pinia'


export const auth = defineStore('auth',()=>{
    const backend_url = 'http://127.0.0.1:5000'
    const token = ref(computed(()=>localStorage.getItem('token')))
    const username = ref(computed(()=>localStorage.getItem('user_details')))

    const isAuthenticated = computed(()=>token.value !== null)

    function setToken(token){
        localStorage.setItem('token',token)
    }

    function setUserDetails(user_dets){
        localStorage.setItem('user_details',user_dets)
    }
    
    async function login(user_details){
        try{
            const response = await fetch(`${backend_url}/api/v1/login`,{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                body: JSON.stringify(user_details)
            })
            if (!response.ok){
                const data = await response.json()
                const rsp = {
                    'status': false,
                    'message': data.message
                }
                return rsp
            }
            else{
                const data = await response.json()
                if (data.user.auth_token){
                    setToken(data.user.auth_token)
                    const user_dets = {
                        'username':data.user.username,
                        'role':data.user.roles[0],
                        'email':data.user.email,
                        'address':data.user.address
                    }
                    setUserDetails(JSON.stringify(user_dets))
                    const rsp = {
                        'status': true,
                        'message': data.message
                    }
                    return rsp
                }
            }
        }
        catch(error){
            console.error(error)
            const rsp = {
                'status': true,
                'message': 'Oops! Something Went Wrong'
            }
            return rsp
        }
    }

    return {login, token, username, isAuthenticated}
});