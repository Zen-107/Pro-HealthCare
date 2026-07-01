import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // อนุญาตให้มือถือในวง LAN เข้า dev server ได้ (ทดสอบกล้องบนมือถือ)
    host: true,
  },
});
