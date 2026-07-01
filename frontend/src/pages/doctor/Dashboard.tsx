import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../../api/client";

interface PatientWithUser {
  patient: {
    id: number;
    user_id: number;
    dob: string | null;
    gender: string | null;
    height_cm: number | null;
    weight_kg: number | null;
    assigned_doctor_id: number | null;
    medical_notes: string | null;
  };
  user: {
    id: number;
    email: string;
    full_name: string;
    role: string;
    phone: string | null;
    is_active: boolean;
  };
}

export default function DoctorDashboard() {
  const [patients, setPatients] = useState<PatientWithUser[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<PatientWithUser[]>("/users/patients")
      .then((r) => setPatients(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-800">👨‍⚕️ ผู้ป่วยของฉัน</h1>
        <p className="mt-1 text-slate-500">ติดตามพัฒนาการและจัดการแผนกายภาพ</p>
      </div>

      {loading && <p className="text-slate-400">กำลังโหลด...</p>}

      {!loading && patients.length === 0 && (
        <div className="card text-center">
          <p className="text-slate-500">ยังไม่มีผู้ป่วยในการดูแล</p>
          <p className="mt-1 text-xs text-slate-400">
            เมื่อผู้ป่วยสมัครแล้ว assigned_doctor_id ชี้มาที่คุณ จะปรากฏที่นี่
          </p>
        </div>
      )}

      {/* Patient list */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
        {patients.map(({ patient, user }) => (
          <Link key={patient.id} to={`/doctor/patient/${patient.id}`} className="card transition hover:shadow-md">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-semibold text-slate-800">{user.full_name}</p>
                <p className="text-sm text-slate-500">{user.email}</p>
              </div>
              <span className={`h-2.5 w-2.5 rounded-full ${user.is_active ? "bg-green-500" : "bg-slate-300"}`} />
            </div>
            <div className="mt-3 flex gap-4 text-xs text-slate-400">
              <span>👤 {patient.gender ?? "-"}</span>
              <span>📏 {patient.height_cm ?? "-"} cm</span>
              <span>⚖️ {patient.weight_kg ?? "-"} kg</span>
            </div>
            {patient.medical_notes && (
              <p className="mt-2 line-clamp-1 text-xs text-slate-400">📝 {patient.medical_notes}</p>
            )}
          </Link>
        ))}
      </div>

      {/* Note */}
      <div className="card bg-amber-50/50">
        <p className="text-sm text-amber-700">
          ⚠️ <strong>Safety First:</strong> การปรับแผนกายภาพต้องได้รับการ Approve จากแพทย์ (Human-in-the-loop)
          — AI ช่วยแนะนำเท่านั้น
        </p>
      </div>
    </div>
  );
}
