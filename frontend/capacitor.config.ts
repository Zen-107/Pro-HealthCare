import type { CapacitorConfig } from "@capacitor/cli";

// ตั้งค่า Capacitor — สำหรับ wrap web app เป็น Android APK (Step 4)
// webDir ชี้ไปผลลัพธ์ build ของ Vite
const config: CapacitorConfig = {
  appId: "com.prohealthcare.app",
  appName: "AI Physio: กายภาพบำบัดที่บ้าน",
  webDir: "dist",
  server: {
    androidScheme: "https",
  },
  plugins: {
    Camera: {
      // ขอ permission กล้องตอนรัน (Android runtime permission)
      permissions: ["camera"],
    },
  },
};

export default config;
