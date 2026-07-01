import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuthStore } from "../../store/auth";
import type { ExercisePlan, PatientStats } from "../../types";
import api from "../../api/client";

// Mock stats — Step 2 จะเชื่อมจาก API จริง
const MOCK_STATS: PatientStats = {
  streak: 7,
  avg_accuracy: 85,
  medals: 3,
};

export default function PatientDashboard() {
  const { user } = useAuthStore();
  const [plans, setPlans] = useState<ExercisePlan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<ExercisePlan[]>("/plans/mine")
      .then((r) => setPlans(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const activePlan = plans.find((p) => p.status === "active");

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold sm:text-3xl">
          สวัสดี, {user?.full_name} 👋
        </h1>
        <p className="text-base-content/60">มาฝึกกายภาพกันวันนี้</p>
      </div>

      {/* Stats */}
      <div className="stats stats-vertical w-full shadow-sm sm:stats-horizontal">
        <div className="stat">
          <div className="stat-figure text-secondary">
            <span className="text-2xl">🔥</span>
          </div>
          <div className="stat-title">วันติดต่อกัน</div>
          <div className="stat-value text-secondary">{MOCK_STATS.streak}</div>
          <div className="stat-desc">Streak</div>
        </div>
        <div className="stat">
          <div className="stat-figure text-success">
            <span className="text-2xl">✅</span>
          </div>
          <div className="stat-title">คะแนนเฉลี่ย</div>
          <div className="stat-value text-success">{MOCK_STATS.avg_accuracy}%</div>
          <div className="stat-desc">Accuracy Score</div>
        </div>
        <div className="stat">
          <div className="stat-figure text-warning">
            <span className="text-2xl">🏆</span>
          </div>
          <div className="stat-title">เหรียญ</div>
          <div className="stat-value text-warning">{MOCK_STATS.medals}</div>
          <div className="stat-desc">Badges</div>
        </div>
      </div>

      {/* Active plan */}
      <div className="card bg-base-100 shadow-sm">
        <div className="card-body p-5">
          <h2 className="card-title text-lg">📋 แผนกายภาพปัจจุบัน</h2>

          {loading && (
            <div className="flex w-full flex-col gap-2">
              <div className="skeleton h-4 w-3/4" />
              <div className="skeleton h-4 w-1/2" />
            </div>
          )}

          {!loading && !activePlan && (
            <div className="alert alert-info">
              <span>ยังไม่มีแผนกายภาพที่ใช้งานอยู่ — กรุณาติดต่อแพทย์ของคุณ</span>
            </div>
          )}

          {!loading && activePlan && (
            <div className="space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="font-semibold">{activePlan.name}</span>
                <span className="badge badge-success badge-sm">{activePlan.status}</span>
              </div>
              <p className="text-sm text-base-content/60">
                {activePlan.items?.length ?? 0} ท่า | {activePlan.start_date} — {activePlan.end_date ?? "ไม่ระบุ"}
              </p>
              {activePlan.items && activePlan.items.length > 0 && (
                <ul className="mt-2 divide-y divide-base-200">
                  {activePlan.items.map((item) => (
                    <li key={item.id} className="flex items-center justify-between py-2.5 text-sm">
                      <span>ท่า #{item.order_index + 1}</span>
                      <span className="badge badge-outline badge-sm">
                        {item.sets} × {item.reps_per_set} reps
                      </span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Quick actions */}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <Link to="/patient/camera" className="btn btn-primary btn-block">
          📷 เริ่มฝึก (เปิดกล้อง)
        </Link>
        <Link to="/patient/progress" className="btn btn-outline btn-block">
          📈 ดูพัฒนาการ
        </Link>
      </div>
    </div>
  );
}
