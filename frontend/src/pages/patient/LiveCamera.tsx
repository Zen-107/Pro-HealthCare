import { useState } from "react";
import { Link } from "react-router-dom";
import SkeletonOverlay from "../../components/SkeletonOverlay";
import AngleChart from "../../components/AngleChart";

type SessionState = "idle" | "running" | "ended";

// Mock feedback จาก AI Coach (สลับเพื่อจำลอง real-time)
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

  const startSession = () => {
    setSessionState("running");
    setReps(0);
    // Step 2: POST /sessions เพื่อสร้าง session จริง
  };

  const endSession = () => {
    setSessionState("ended");
    // Step 2: PATCH /sessions/{id} status=completed
  };

  // Mock: นับ rep แบบจำลอง + เปลี่ยน accuracy/feedback ตาม rep
  const addRep = () => {
    setReps((r) => r + 1);
    setAccuracy(() => Math.floor(80 + Math.random() * 18));
    setFeedbackIdx((i) => (i + 1) % MOCK_FEEDBACKS.length);
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

      {/* Camera area */}
      <SkeletonOverlay />

      {/* Live feedback (mock) */}
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

              {/* AI Coach mock feedback */}
              <div className="chat chat-start mt-2">
                <div className="chat-bubble chat-bubble-primary">
                  🗣️ <strong>AI Coach:</strong> {MOCK_FEEDBACKS[feedbackIdx]}
                </div>
              </div>
            </div>
          </div>
          <AngleChart />
        </div>
      )}

      {/* Controls */}
      <div className="grid grid-cols-2 gap-3">
        {sessionState === "idle" && (
          <button onClick={startSession} className="btn btn-primary col-span-2">
            ▶️ เริ่มเซสชันฝึก
          </button>
        )}
        {sessionState === "running" && (
          <>
            <button onClick={addRep} className="btn btn-outline">
              + นับ rep (mock)
            </button>
            <button onClick={endSession} className="btn btn-error">
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
