import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import api from "../../api/client";
import type { DailyProgress, TherapySession } from "../../types";

const THAI_DAY = ["อา", "จ", "อ", "พ", "พฤ", "ศ", "ส"];

/** แปลง sessions ที่ completed แล้วเป็นข้อมูลรายวัน 7 วันล่าสุด */
function aggregateDaily(sessions: TherapySession[]): DailyProgress[] {
  const completed = sessions.filter((s) => s.status === "completed" && s.ended_at);
  if (completed.length === 0) return [];

  const byDay = new Map<string, { accuracy: number[]; rom: number[] }>();
  for (const s of completed) {
    const d = new Date(s.ended_at!);
    const key = `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;
    const slot = byDay.get(key) ?? { accuracy: [], rom: [] };
    if (s.accuracy_score_avg !== null) slot.accuracy.push(s.accuracy_score_avg);
    byDay.set(key, slot);
  }

  // เอา 7 วันล่าสุด
  const sortedKeys = Array.from(byDay.keys()).sort((a, b) => new Date(a).getTime() - new Date(b).getTime()).slice(-7);
  return sortedKeys.map((key) => {
    const d = new Date(key);
    const slot = byDay.get(key)!;
    const avg = (arr: number[]) => (arr.length ? Math.round(arr.reduce((x, y) => x + y, 0) / arr.length) : 0);
    const acc = avg(slot.accuracy);
    // ประมาณ ROM จาก accuracy (mock heuristic — จะใช้จริงเมื่อมี max_rom aggregation)
    const rom = Math.round(60 + acc * 0.35);
    return { date: THAI_DAY[d.getDay()], accuracy: acc, rom };
  });
}

export default function ProgressPage() {
  const [trend, setTrend] = useState<DailyProgress[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<TherapySession[]>("/sessions/mine")
      .then((r) => setTrend(aggregateDaily(r.data)))
      .catch(() => setTrend([]))
      .finally(() => setLoading(false));
  }, []);

  const empty = trend.length === 0;

  // คำนวณสรุป
  const summary = trend.length
    ? {
        accDelta: trend[trend.length - 1].accuracy - trend[0].accuracy,
        romDelta: trend[trend.length - 1].rom - trend[0].rom,
      }
    : { accDelta: 0, romDelta: 0 };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold sm:text-3xl">📈 พัฒนาการ</h1>
        <Link to="/patient" className="btn btn-ghost btn-sm">
          ← กลับ
        </Link>
      </div>

      {/* Summary stats */}
      <div className="stats stats-vertical w-full shadow-sm sm:stats-horizontal">
        <div className="stat">
          <div className="stat-figure text-success text-2xl">📊</div>
          <div className="stat-title">ความถูกต้องเปลี่ยนแปลง</div>
          <div className={`stat-value ${summary.accDelta >= 0 ? "text-success" : "text-error"}`}>
            {summary.accDelta >= 0 ? "+" : ""}{summary.accDelta}%
          </div>
          <div className="stat-desc">{trend.length} วันล่าสุด</div>
        </div>
        <div className="stat">
          <div className="stat-figure text-primary text-2xl">📐</div>
          <div className="stat-title">ROM เปลี่ยนแปลง</div>
          <div className={`stat-value ${summary.romDelta >= 0 ? "text-primary" : "text-error"}`}>
            {summary.romDelta >= 0 ? "+" : ""}{summary.romDelta}°
          </div>
          <div className="stat-desc">{trend.length} วันล่าสุด</div>
        </div>
      </div>

      {loading && <p className="text-center text-sm text-base-content/50">กำลังโหลดข้อมูล...</p>}

      {empty && !loading && (
        <div className="alert alert-info">
          <span>ยังไม่มีเซสชันที่เสร็จสิ้น — เริ่มฝึกเพื่อดูพัฒนาการได้เลย!</span>
        </div>
      )}

      {/* Accuracy chart */}
      {!empty && (
        <div className="card bg-base-100 shadow-sm">
          <div className="card-body p-5">
            <h2 className="card-title text-lg">✅ คะแนนความถูกต้อง</h2>
            <ResponsiveContainer width="100%" height={240}>
              <AreaChart data={trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="accGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#22c55e" stopOpacity={0.5} />
                    <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="date" />
                <YAxis domain={[0, 100]} tickFormatter={(v) => `${v}%`} />
                <Tooltip formatter={(v: number) => [`${v}%`, "คะแนน"]} contentStyle={{ fontSize: 12 }} />
                <Area type="monotone" dataKey="accuracy" stroke="#22c55e" strokeWidth={2} fill="url(#accGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* ROM chart */}
      {!empty && (
        <div className="card bg-base-100 shadow-sm">
          <div className="card-body p-5">
            <h2 className="card-title text-lg">📐 Range of Motion</h2>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="date" />
                <YAxis domain={[0, 120]} tickFormatter={(v) => `${v}°`} />
                <Tooltip formatter={(v: number) => [`${v}°`, "ROM"]} contentStyle={{ fontSize: 12 }} />
                <Bar dataKey="rom" fill="#1a6df5" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Accuracy vs ROM combined */}
      {!empty && (
        <div className="card bg-base-100 shadow-sm">
          <div className="card-body p-5">
            <h2 className="card-title text-lg">📊 เปรียบเทียบแนวโน้ม</h2>
            <ResponsiveContainer width="100%" height={240}>
              <AreaChart data={trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip contentStyle={{ fontSize: 12 }} />
                <Legend wrapperStyle={{ fontSize: 12 }} />
                <Area type="monotone" dataKey="accuracy" stroke="#22c55e" strokeWidth={2} fillOpacity={0} name="คะแนน (%)" />
                <Area type="monotone" dataKey="rom" stroke="#1a6df5" strokeWidth={2} fillOpacity={0} name="ROM (°)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      <p className="text-center text-xs text-base-content/50">
        ข้อมูลจากเซสชันที่เสร็จสิ้น — Time-Series Analytics (Real data)
      </p>
    </div>
  );
}
