import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "../store/auth";

export default function Layout({ children }: { children: React.ReactNode }) {
  const { user, logout } = useAuthStore();
  const navigate = useNavigate();
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const dashboardPath = user?.role === "doctor" ? "/doctor" : "/patient";

  return (
    <div className="drawer">
      <input id="layout-drawer" type="checkbox" className="drawer-toggle" checked={drawerOpen} readOnly />

      <div className="drawer-content flex min-h-screen flex-col">
        {/* Navbar */}
        <div className="navbar sticky top-0 z-30 bg-base-100 shadow-sm">
          <div className="navbar-start">
            {/* Hamburger (mobile) */}
            <label htmlFor="layout-drawer" className="btn btn-ghost btn-circle lg:hidden" onClick={() => setDrawerOpen(!drawerOpen)}>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </label>
            <Link to={dashboardPath} className="btn btn-ghost text-lg font-bold">
              🏋️ AI Physio
            </Link>
          </div>

          <div className="navbar-center hidden lg:flex">
            {/* Desktop nav links */}
            {user?.role === "patient" && (
              <ul className="menu menu-horizontal menu-md gap-1">
                <li><Link to="/patient">Dashboard</Link></li>
                <li><Link to="/patient/camera">📹 ฝึกกายภาพ</Link></li>
                <li><Link to="/patient/progress">📈 พัฒนาการ</Link></li>
              </ul>
            )}
            {user?.role === "doctor" && (
              <ul className="menu menu-horizontal menu-md gap-1">
                <li><Link to="/doctor">Dashboard</Link></li>
              </ul>
            )}
          </div>

          <div className="navbar-end gap-2">
            {user && (
              <div className="hidden items-center gap-2 sm:flex">
                <span className="text-sm">{user.full_name}</span>
                <span className="badge badge-sm">{user.role === "doctor" ? "แพทย์" : "ผู้ป่วย"}</span>
              </div>
            )}
            <button onClick={handleLogout} className="btn btn-ghost btn-sm">
              ออกจากระบบ
            </button>
          </div>
        </div>

        {/* Content */}
        <main className="mx-auto w-full max-w-7xl flex-1 px-4 py-6">{children}</main>

        {/* Footer */}
        <footer className="border-t border-base-300 bg-base-200 py-4 text-center text-xs text-base-content/60">
          AI Physio — ช่วยฟื้นฟูกายภาพบำบัดที่บ้าน © 2026
        </footer>
      </div>

      {/* Mobile drawer sidebar */}
      <div className="drawer-side z-40">
        <label htmlFor="layout-drawer" aria-label="close sidebar" className="drawer-overlay" onClick={() => setDrawerOpen(false)} />
        <ul className="menu bg-base-100 min-h-full w-64 p-4">
          <li className="mb-2 text-lg font-bold text-primary">🏋️ AI Physio</li>
          {user?.role === "patient" && (
            <>
              <li><Link to="/patient" onClick={() => setDrawerOpen(false)}>📊 Dashboard</Link></li>
              <li><Link to="/patient/camera" onClick={() => setDrawerOpen(false)}>📹 ฝึกกายภาพ</Link></li>
              <li><Link to="/patient/progress" onClick={() => setDrawerOpen(false)}>📈 พัฒนาการ</Link></li>
            </>
          )}
          {user?.role === "doctor" && (
            <li><Link to="/doctor" onClick={() => setDrawerOpen(false)}>📊 Dashboard</Link></li>
          )}
          <div className="divider" />
          {user && (
            <div className="px-2">
              <span className="badge badge-lg">{user.role === "doctor" ? "แพทย์" : "ผู้ป่วย"}</span>
              <p className="mt-1 text-sm">{user.full_name}</p>
            </div>
          )}
        </ul>
      </div>
    </div>
  );
}
