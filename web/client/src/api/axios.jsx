import axios from "axios";

// backend port
const instance = axios.create({
  baseURL: "http://localhost:5000",
});
instance.defaults.withCredentials = true;

export default instance;
