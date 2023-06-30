import axios from 'axios';

const DEV_MODE = import.meta.env.DEV

const API_BASE_URL = DEV_MODE ? 'http://localhost:8000' : window.location.origin;
export const api = axios.create({
  baseURL: API_BASE_URL
});


export interface NetInterface {
  name: string
  address: string
  netmask: string
  family: number
  prefix_length: number
}
export interface Host {
  ip: string
  mac: string
  vendor: string
  hostname: string
}
