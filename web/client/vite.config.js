import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 8000,
    watch: {
      usePolling: true, // Enable polling for file changes
    },
  },
  preview: {
    host: true,
    port: 8000
  }
});
