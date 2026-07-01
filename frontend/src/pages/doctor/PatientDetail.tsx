import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../../api/client";
import type { ClinicalReport, ExercisePlan } from "../../types";

export default function DoctorPatientDetail() {
  const { patientId } = useParams<{ patientId: string }>();
  const [plans, setPlans] = useState<ExercisePlan[]>([]);
  const [reports, setReports] = useState<ClinicalReport[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!patientId) return;
    Promise.all([
      api.get<ExercisePlan[]>(`/plans/patient/${patientId}`),
      api.get<ClinicalReport[]>(`/reports/patient/${patientId}`),
    ])
      .then(([p, r]) => {
        setPlans(p.data);
        setReports(r.data);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [patientId]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-800">👤 รายละเอียดผู้ป่วย #{patientId}</h1>
        <Link to="/doctor" className="btn-secondary text-sm">
          ← กลับ
        </Link>
      </div>

      {/* Plans */}
      <div className="card">
        <h2 className="mb-3 text-lg font-semibold text-slate-700">📋 แผนกายภาพ</h2>
        {loading && <p className="text-sm text-slate-400">กำลังโหลด...</p>}
        {!loading && plans.length === 0 && (
          <p className="text-sm text-slate-400">ยังไม่มีแผน — สร้างแผนใหม่ได้จาก API (UI สร้างแผนอยู่ใน Step ต่อไป)</p>
        )}
        <div className="space-y-2">
          {plans.map((plan) => (
            <div key={plan.id} className="rounded-lg border border-slate-200 p-3">
              <div className="flex items-center justify-between">
                <span className="font-medium text-slate-800">{plan.name}</span>
                <span className={`rounded-full px-2 py-0.5 text-xs ${
                  plan.status === "active" ? "bg-green-100 text-green-700"
                  : plan.status === "draft" ? "bg-slate-100 text-slate-600"
                  : "bg-amber-100 text-amber-700"
                }`}>
                  {plan.status}
                </span>
              </div>
              <p className="mt-1 text-xs text-slate-500">
                {plan.items?.length ?? 0} ท่า | {plan.start_date ?? "-"} → {plan.end_date ?? "-"}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Reports */}
      <div className="card">
        <h2 className="mb-3 text-lg font-semibold text-slate-700">📄 รายงานทางคลินิก</h2>
        {!loading && reports.length === 0 && (
          <div className="rounded-lg bg-slate-50 p-4 text-center text-sm text-slate-400">
            ยังไม่มีรายงาน — 🤖 AI Reporter (Agent 3) จะสร้างอัตโนมัติเมื่อจบเซสชัน (Step 3)
          </div>
        )}
        <div className="space-y-2">
          {reports.map((rep) => (
            <div key={rep.id} className="rounded-lg border border-slate-200 p-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-700">
                  {rep.period_start ?? "session"} → {rep.period_end ?? "-"}
                </span>
                {rep.pdf_path && (
                  <a href={rep.pdf_path} className="text-xs text-brand-600 underline">ดู PDF</a>
                )}
              </div>
              {rep.llm_note && <p className="mt-1 text-sm text-slate-600">{rep.llm_note}</p>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
