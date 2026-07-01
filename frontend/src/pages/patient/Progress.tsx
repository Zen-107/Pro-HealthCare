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
import type { DailyProgress } from "../../types";

/**
 * MOCK — หน้าพัฒนาการ (Progress)
 * Step 2-3: จะเชื่อม Time-Series data จาก /sessions/mine และ /reports
 */
const TREND: DailyProgress[] = [
  { date: "จ", accuracy: 62, rom: 70 },
  { date: "อ", accuracy: 68, rom: 75 },
  { date: "พ", accuracy: 65, rom: 78 },
  { date: "พฤ", accuracy: 74, rom: 82 },
  { date: "ศ", accuracy: 78, rom: 85 },
  { date: "ส", accuracy: 81, rom: 88 },
  { date: "อา", accuracy: 85, rom: 92 },
];

export default function ProgressPage() {
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
          <div className="stat-title">ความถูกต้องดีขึ้น</div>
          <div className="stat-value text-success">+23%</div>
          <div className="stat-desc">7 วันล่าสุด</div>
        </div>
        <div className="stat">
          <div className="stat-figure text-primary text-2xl">📐</div>
          <div className="stat-title">ROM ดีขึ้น</div>
          <div className="stat-value text-primary">+22°</div>
          <div className="stat-desc">7 วันล่าสุด</div>
        </div>
        <div className="stat">
          <div className="stat-figure text-warning text-2xl">🔮</div>
          <div className="stat-title">พยากรณ์ฟื้นตัว</div>
          <div className="stat-value text-warning">~3</div>
          <div className="stat-desc">สัปดาห์</div>
        </div>
      </div>

      {/* Accuracy chart */}
      <div className="card bg-base-100 shadow-sm">
        <div className="card-body p-5">
          <h2 className="card-title text-lg">✅ คะแนนความถูกต้อง (7 วันล่าสุด)</h2>
          <ResponsiveContainer width="100%" height={240}>
            <AreaChart data={TREND} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
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

      {/* ROM chart */}
      <div className="card bg-base-100 shadow-sm">
        <div className="card-body p-5">
          <h2 className="card-title text-lg">📐 Range of Motion (7 วันล่าสุด)</h2>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={TREND} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="date" />
              <YAxis domain={[0, 120]} tickFormatter={(v) => `${v}°`} />
              <Tooltip formatter={(v: number) => [`${v}°`, "ROM"]} contentStyle={{ fontSize: 12 }} />
              <Bar dataKey="rom" fill="#1a6df5" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Accuracy vs ROM combined */}
      <div className="card bg-base-100 shadow-sm">
        <div className="card-body p-5">
          <h2 className="card-title text-lg">📊 เปรียบเทียบแนวโน้ม</h2>
          <ResponsiveContainer width="100%" height={240}>
            <AreaChart data={TREND} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
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

      {/* Clinical note mock */}
      <div className="alert alert-warning alert-soft flex flex-col items-start gap-1">
        <h2 className="text-lg font-semibold">📄 บันทึกจากแพทย์</h2>
        <p className="text-sm">
          “พัฒนาการดีขึ้นชัดเจน ให้ทำท่าใหม่ที่ยากขึ้น และคงระดับ 3 ครั้ง/สัปดาห์” — แพทย์จะ Approve แผนใหม่ผ่าน Dashboard
        </p>
        <p className="text-xs text-base-content/60">
          🤖 AI Reporter จะสรุปอัตโนมัติใน Step 3
        </p>
      </div>

      <p className="text-center text-xs text-base-content/50">
        ข้อมูล {TREND.length} วัน — Time-Series Analytics (เชื่อมจริงใน Step 2)
      </p>
    </div>
  );
}
