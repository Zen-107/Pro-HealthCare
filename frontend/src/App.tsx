import { lazy, Suspense, useEffect } from "react";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { useAuthStore } from "./store/auth";
import Layout from "./components/Layout";
import { GuestGuard, RoleGuard } from "./components/Guards";

const LoginPage = lazy(() => import("./pages/auth/Login"));
const PatientDashboard = lazy(() => import("./pages/patient/Dashboard"));
const LiveCameraPage = lazy(() => import("./pages/patient/LiveCamera"));
const ProgressPage = lazy(() => import("./pages/patient/Progress"));
const DoctorDashboard = lazy(() => import("./pages/doctor/Dashboard"));
const DoctorPatientDetail = lazy(() => import("./pages/doctor/PatientDetail"));

function Loading() {
  return (
    <div className="flex h-full items-center justify-center text-slate-400">กำลังโหลด...</div>
  );
}

export default function App() {
  const restore = useAuthStore((s) => s.restore);

  useEffect(() => {
    restore();
  }, [restore]);

  return (
    <BrowserRouter>
      <Suspense fallback={<Loading />}>
        <Routes>
          {/* หน้าสาธารณะ */}
          <Route element={<GuestGuard />}>
            <Route path="/login" element={<LoginPage />} />
          </Route>

          {/* หน้าผู้ป่วย */}
          <Route element={<RoleGuard allowed={["patient"]} />}>
            <Route
              path="/patient"
              element={
                <Layout>
                  <PatientDashboard />
                </Layout>
              }
            />
            <Route
              path="/patient/camera"
              element={
                <Layout>
                  <LiveCameraPage />
                </Layout>
              }
            />
            <Route
              path="/patient/progress"
              element={
                <Layout>
                  <ProgressPage />
                </Layout>
              }
            />
          </Route>

          {/* หน้าแพทย์ */}
          <Route element={<RoleGuard allowed={["doctor"]} />}>
            <Route
              path="/doctor"
              element={
                <Layout>
                  <DoctorDashboard />
                </Layout>
              }
            />
            <Route
              path="/doctor/patient/:patientId"
              element={
                <Layout>
                  <DoctorPatientDetail />
                </Layout>
              }
            />
          </Route>

          {/* ค่าเริ่มต้น */}
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
