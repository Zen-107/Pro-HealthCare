import { useState, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../../store/auth";

export default function LoginPage() {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [role, setRole] = useState("patient");
  const [error, setError] = useState("");
  const { login, register, loading } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      if (isRegister) {
        await register({ email, password, full_name: fullName, role });
      } else {
        await login(email, password);
      }
      const user = useAuthStore.getState().user;
      navigate(user?.role === "doctor" ? "/doctor" : "/patient");
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || "เกิดข้อผิดพลาด";
      setError(String(msg));
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-brand-50 to-slate-100 px-4">
      <div className="card w-full max-w-md">
        {/* Header */}
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-bold text-slate-800">🏋️ AI Physio</h1>
          <p className="mt-1 text-sm text-slate-500">กายภาพบำบัดที่บ้าน — ช่วยฟื้นฟูด้วย AI</p>
        </div>

        {/* Tab */}
        <div className="mb-4 flex rounded-lg bg-slate-100 p-1">
          <button
            onClick={() => { setIsRegister(false); setError(""); }}
            className={`flex-1 rounded-md py-1.5 text-sm font-medium transition ${!isRegister ? "bg-white shadow-sm text-brand-600" : "text-slate-500"}`}
          >
            เข้าสู่ระบบ
          </button>
          <button
            onClick={() => { setIsRegister(true); setError(""); }}
            className={`flex-1 rounded-md py-1.5 text-sm font-medium transition ${isRegister ? "bg-white shadow-sm text-brand-600" : "text-slate-500"}`}
          >
            สมัครใช้งาน
          </button>
        </div>

        {error && (
          <div className="mb-3 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">{error}</div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3">
          {isRegister && (
            <>
              <div>
                <label className="label">ชื่อ-นามสกุล</label>
                <input className="input" value={fullName} onChange={(e) => setFullName(e.target.value)} required />
              </div>
              <div>
                <label className="label">บทบาท</label>
                <select className="input" value={role} onChange={(e) => setRole(e.target.value)}>
                  <option value="patient">ผู้ป่วย</option>
                  <option value="doctor">แพทย์</option>
                </select>
              </div>
            </>
          )}
          <div>
            <label className="label">อีเมล</label>
            <input className="input" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>
          <div>
            <label className="label">รหัสผ่าน</label>
            <input className="input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={6} />
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? "กำลังดำเนินการ..." : isRegister ? "สมัครใช้งาน" : "เข้าสู่ระบบ"}
          </button>
        </form>
      </div>
    </div>
  );
}
