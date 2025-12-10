import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  preview: {
    allowedHosts: [
      "labelforce-frontend-5oaq.onrender.com",  // ADD THIS
    ],
    port: 10000,
  },
});
