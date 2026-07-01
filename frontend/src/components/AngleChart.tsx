/**
 * MOCK — กราฟมุมข้อต่อแบบ Real-time (สไตล์ Oscilloscope)
 * Step 2: จะเชื่อม Recharts + real data จาก /sessions/{id}/angles
 */
import { LineChart, Line, XAxis, YAxis, ReferenceLine, ResponsiveContainer, Tooltip } from "recharts";
import type { AngleDataPoint } from "../types";

// mock data
const data: AngleDataPoint[] = [
  { time: 0, angle: 95 },
  { time: 500, angle: 92 },
  { time: 1000, angle: 88 },
  { time: 1500, angle: 85 },
  { time: 2000, angle: 90 },
  { time: 2500, angle: 93 },
  { time: 3000, angle: 88 },
  { time: 3500, angle: 82 },
  { time: 4000, angle: 78 },
  { time: 4500, angle: 80 },
  { time: 5000, angle: 85 },
  { time: 5500, angle: 90 },
];

const TARGET_ANGLE = 90;

export default function AngleChart() {
  return (
    <div className="card bg-base-100 shadow-sm">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-sm font-semibold">📊 มุมข้อต่อ</h3>
        <span className="badge badge-ghost badge-sm">Mock Data</span>
      </div>
      <div className="rounded-lg bg-base-300 p-2">
        <ResponsiveContainer width="100%" height={130}>
          <LineChart data={data}>
            <XAxis dataKey="time" hide />
            <YAxis domain={[60, 110]} tick={{ fontSize: 10 }} width={30} />
            <Tooltip
              formatter={(v: number) => [`${v}°`, "มุม"]}
              labelFormatter={(t: number) => `${t / 1000}s`}
              contentStyle={{ fontSize: 12 }}
            />
            <ReferenceLine
              y={TARGET_ANGLE}
              stroke="#22c55e"
              strokeDasharray="4 4"
              label={{ value: `target ${TARGET_ANGLE}°`, position: "right", fill: "#22c55e", fontSize: 10 }}
            />
            <Line
              type="monotone"
              dataKey="angle"
              stroke="#1a6df5"
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
