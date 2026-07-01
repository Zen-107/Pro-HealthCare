/** API types ที่ใช้ร่วมกัน */
export interface User {
  id: number;
  email: string;
  full_name: string;
  role: "patient" | "doctor" | "admin";
  phone: string | null;
  is_active: boolean;
}

export interface Token {
  access_token: string;
  token_type: string;
  role: string;
  user_id: number;
}

export interface Exercise {
  id: number;
  name: string;
  name_th: string | null;
  category: string | null;
  difficulty: string;
  target_joints: string[] | null;
  ideal_angles: Record<string, { min?: number; max?: number; target: number }> | null;
  instructions: string | null;
  video_url: string | null;
}

export interface PlanItem {
  id: number;
  plan_id: number;
  exercise_id: number;
  sets: number;
  reps_per_set: number;
  hold_seconds: number | null;
  frequency_per_week: number;
  order_index: number;
}

export interface ExercisePlan {
  id: number;
  patient_id: number;
  doctor_id: number | null;
  name: string;
  status: "draft" | "active" | "paused" | "completed" | "cancelled";
  start_date: string | null;
  end_date: string | null;
  items?: PlanItem[];
}

export interface TherapySession {
  id: number;
  patient_id: number;
  plan_id: number | null;
  started_at: string;
  ended_at: string | null;
  status: "in_progress" | "completed" | "abandoned";
  total_reps: number;
  accuracy_score_avg: number | null;
  device_info: string | null;
}

export interface ClinicalReport {
  id: number;
  patient_id: number;
  session_id: number | null;
  period_start: string | null;
  period_end: string | null;
  summary_json: Record<string, unknown> | null;
  llm_note: string | null;
  pdf_path: string | null;
  created_by_agent: string | null;
}

/** Patient profile + user account — สำหรับหน้าแพทย์ */
export interface PatientWithUser {
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
  user: User;
}

/** Mock data types — สำหรับ charts (จะเชื่อม API จริงใน Step 2) */
export interface AngleDataPoint {
  time: number;
  angle: number;
}

export interface DailyProgress {
  date: string;
  accuracy: number;
  rom: number;
}

export interface PatientStats {
  streak: number;
  avg_accuracy: number;
  medals: number;
}
