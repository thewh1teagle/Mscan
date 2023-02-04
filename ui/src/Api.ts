import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000' // window.location.origin // ;
const api = axios.create({
  baseURL: API_BASE_URL
});


export async function getInterfaces() {
    const res = await api.get('/interfaces')
    return res.data
}

export async function scan(iface: any) {
    const res = await api.post('/scan', iface)
    return res.data
}

