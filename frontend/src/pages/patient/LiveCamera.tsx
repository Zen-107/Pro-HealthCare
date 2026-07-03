import { useState } from "react";
import { Link } from "react-router-dom";
import SkeletonOverlay from "../../components/SkeletonOverlay";
import AngleChart from "../../components/AngleChart";
import api from "../../api/client";
import type { TherapySession } from "../../types";

type SessionState = "idle" | "running" | "ended";

// Mock feedback จาก AI Coach (จะเปลี่ยนเป็น LLM จริงใน Step 3)
const MOCK_FEEDBACKS = [
  "ทำได้ดีมาก! งอเข่าให้สุดระยะอีกนิดนะครับ",
  "ดีเลย! รักษาจังหวะการหายใจไว้",
  "เก่งมาก! พยายามตั้ง 90 องศา",
];

export default function LiveCameraPage() {
  const [sessionState, setSessionState] = useState<SessionState>("idle");
  const [reps, setReps] = useState(0);
  const [accuracy, setAccuracy] = useState(92);
  const [feedbackIdx, setFeedbackIdx] = useState(0);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [exerciseId, setExerciseId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const startSession = async () => {
    setLoading(true);
    setError("");
    try {
      // เลือกท่าแรกจากแผน active (ถ้ามี) — ไม่งั้นใช้ exercise_id แรกที่มี
      let exId: number | null = null;
      try {
        const plans = await api.get<{ id: number; status: string; items?: { exercise_id: number }[] }[]>("/plans/mine");
        const active = plans.data.find((p) => p.status === "active");
        exId = active?.items?.[0]?.exercise_id ?? null;
      } catch {
        // ถ้าไม่มีแผน ลองดึง exercise แรกจากคลัง
        const ex = await api.get<{ id: number }[]>("/exercises");
        exId = ex.data[0]?.id ?? null;
      }
      setExerciseId(exId);

      const res = await api.post<TherapySession>("/sessions", { device_info: "web" });
      setSessionId(res.data.id);
      setReps(0);
      setSessionState("running");
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || "เริ่มเซสชันไม่สำเร็จ";
      setError(String(msg));
    } finally {
      setLoading(false);
    }
  };

  const endSession = async () => {
    if (!sessionId) return;
    setLoading(true);
    try {
      const avg = reps > 0 ? Math.round(accuracy * 100) / 100 : null;
      await api.patch(`/sessions/${sessionId}`, {
        status: "completed",
        total_reps: reps,
        accuracy_score_avg: avg,
      });
      setSessionState("ended");
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || "จบเซสชันไม่สำเร็จ";
      setError(String(msg));
    } finally {
      setLoading(false);
    }
  };

  const addRep = async () => {
    if (!sessionId || !exerciseId) return;
    const newReps = reps + 1;
    const newAcc = Math.floor(80 + Math.random() * 18);
    try {
      await api.post(`/sessions/${sessionId}/reps`, {
        exercise_id: exerciseId,
        rep_number: newReps,
        accuracy_score: newAcc,
        quality: newAcc >= 85 ? "good" : newAcc >= 70 ? "acceptable" : "poor",
      });
      setReps(newReps);
      setAccuracy(newAcc);
      setFeedbackIdx((i) => (i + 1) % MOCK_FEEDBACKS.length);
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || "บันทึก rep ไม่สำเร็จ";
      setError(String(msg));
    }
  };

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold sm:text-3xl">📷 ฝึกกายภาพ</h1>
        <Link to="/patient" className="btn btn-ghost btn-sm">
          ← กลับ
        </Link>
      </div>

      {error && (
        <div className="alert alert-error">
          <span>{error}</span>
          <button onClick={() => setError("")} className="btn btn-ghost btn-xs">ปิด</button>
        </div>
      )}

      {/* Camera area */}
      <SkeletonOverlay />

      {/* Live feedback */}
      {sessionState === "running" && (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
          <div className="card bg-base-100 shadow-sm lg:col-span-2">
            <div className="card-body p-5">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-base-content/60">คะแนนความถูกต้อง</p>
                  <p className="text-4xl font-bold text-success">{accuracy}%</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-base-content/60">จำนวนครั้ง</p>
                  <p className="text-4xl font-bold text-primary">{reps}</p>
                </div>
              </div>

              <div className="chat chat-start mt-2">
                <div className="chat-bubble chat-bubble-primary">
                  🗣️ <strong>AI Coach:</strong> {MOCK_FEEDBACKS[feedbackIdx]}
                </div>
              </div>
            </div>
          </div>
          {sessionId && <AngleChart sessionId={sessionId} />}
        </div>
      )}

      {/* Controls */}
      <div className="grid grid-cols-2 gap-3">
        {sessionState === "idle" && (
          <button onClick={startSession} disabled={loading} className="btn btn-primary col-span-2">
            {loading ? "กำลังเริ่ม..." : "▶️ เริ่มเซสชันฝึก"}
          </button>
        )}
        {sessionState === "running" && (
          <>
            <button onClick={addRep} disabled={loading} className="btn btn-outline">
              + นับ rep
            </button>
            <button onClick={endSession} disabled={loading} className="btn btn-error">
              ⏹️ จบเซสชัน
            </button>
          </>
        )}
      </div>

      {sessionState === "ended" && (
        <div className="alert alert-success">
          <span>🎉 จบเซสชันแล้ว! ทำได้ {reps} ครั้ง</span>
          <div>
            <Link to="/patient/progress" className="btn btn-sm btn-primary">
              ดูพัฒนาการ →
            </Link>
          </div>
        </div>
      )}

      {/* PDPA note */}
      <div className="alert alert-info alert-soft">
        <span className="text-xs">
          🔒 PDPA: ประมวลผลภาพที่เครื่อง (On-device) ส่งขึ้นเฉพาะค่ามุมข้อต่อ (JSON)
        </span>
      </div>
    </div>
  );
}
