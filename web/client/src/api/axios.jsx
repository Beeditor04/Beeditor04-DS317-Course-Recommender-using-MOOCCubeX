import axios from "axios";

// backend port
const instance = axios.create({
  baseURL: "http://localhost:3000",
});
instance.defaults.withCredentials = true;

export default instance;
