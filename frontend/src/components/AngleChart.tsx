/**
 * กราฟมุมข้อต่อแบบ Real-time — ดึง time-series จาก /sessions/{id}/angles
 */
import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, ReferenceLine, ResponsiveContainer, Tooltip } from "recharts";
import api from "../api/client";
import type { AngleDataPoint } from "../types";

const TARGET_ANGLE = 90;
const POLL_MS = 2000;

interface AngleResponse {
  timestamp_ms: number;
  joint_name: string;
  angle_value: number;
}

export default function AngleChart({ sessionId }: { sessionId: number }) {
  const [data, setData] = useState<AngleDataPoint[]>([]);

  useEffect(() => {
    let active = true;
    const load = async () => {
      try {
        const res = await api.get<AngleResponse[]>(`/sessions/${sessionId}/angles`);
        if (!active) return;
        // เลือก joint แรกที่เจอ (เช่น left_knee) และแปลงเป็นรูปแบบกราฟ
        const joints = Array.from(new Set(res.data.map((d) => d.joint_name)));
        const target = joints[0];
        const points = res.data
          .filter((d) => d.joint_name === target)
          .map((d) => ({ time: d.timestamp_ms, angle: d.angle_value }));
        setData(points);
      } catch {
        // ยังไม่มีข้อมูล — ปล่อยว่างไว้
      }
    };
    load();
    const timer = setInterval(load, POLL_MS);
    return () => {
      active = false;
      clearInterval(timer);
    };
  }, [sessionId]);

  return (
    <div className="card bg-base-100 shadow-sm">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="text-sm font-semibold">📊 มุมข้อต่อ</h3>
        <span className="badge badge-ghost badge-sm">
          {data.length > 0 ? `${data.length} จุด` : "รอข้อมูล"}
        </span>
      </div>
      <div className="rounded-lg bg-base-300 p-2">
        <ResponsiveContainer width="100%" height={130}>
          <LineChart data={data}>
            <XAxis dataKey="time" hide />
            <YAxis domain={[0, 180]} tick={{ fontSize: 10 }} width={30} />
            <Tooltip
              formatter={(v: number) => [`${v}°`, "มุม"]}
              labelFormatter={(t: number) => `${(t / 1000).toFixed(1)}s`}
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
