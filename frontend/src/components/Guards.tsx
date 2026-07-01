import { Navigate, Outlet } from "react-router-dom";
import { useAuthStore } from "../store/auth";

export function RoleGuard({ allowed }: { allowed: string[] }) {
  const user = useAuthStore((s) => s.user);
  if (!user) return <Navigate to="/login" replace />;
  if (!allowed.includes(user.role)) {
    const target = user.role === "doctor" ? "/doctor" : "/patient";
    return <Navigate to={target} replace />;
  }
  return <Outlet />;
}

export function GuestGuard() {
  const user = useAuthStore((s) => s.user);
  if (user) {
    const target = user.role === "doctor" ? "/doctor" : "/patient";
    return <Navigate to={target} replace />;
  }
  return <Outlet />;
}
