/**
 * MOCK — Skeleton Overlay สำหรับหน้า Live Camera
 * Step 2: จะเชื่อม MediaPipe Pose จริง + canvas วาด skeleton
 */
export default function SkeletonOverlay() {
  return (
    <div className="mockup-browser border border-base-300 bg-base-200">
      <div className="mockup-browser-toolbar">
        <div className="input input-bordered input-sm mx-auto w-48 bg-base-200 text-center text-xs">
          📷 เปิดกล้อง — MediaPipe Pose (Step 2)
        </div>
      </div>
      <div className="relative flex aspect-video w-full items-center justify-center bg-base-300 max-h-[70vh] sm:max-h-none">
        {/* mock skeleton lines */}
        <svg className="pointer-events-none absolute inset-0 h-full w-full opacity-15" viewBox="0 0 320 240">
          <circle cx="160" cy="60" r="8" fill="currentColor" className="text-primary" />
          <line x1="160" y1="68" x2="160" y2="130" stroke="currentColor" strokeWidth="3" className="text-primary" />
          <line x1="160" y1="80" x2="120" y2="120" stroke="currentColor" strokeWidth="3" className="text-primary" />
          <line x1="160" y1="80" x2="200" y2="120" stroke="currentColor" strokeWidth="3" className="text-primary" />
          <line x1="160" y1="130" x2="130" y2="190" stroke="currentColor" strokeWidth="3" className="text-primary" />
          <line x1="160" y1="130" x2="190" y2="190" stroke="currentColor" strokeWidth="3" className="text-primary" />
        </svg>
        {/* center placeholder */}
        <div className="flex flex-col items-center gap-2 text-base-content/50">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-base-100 shadow">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9a2.25 2.25 0 00-2.25-2.25h-9A2.25 2.25 0 002.25 7.5v9a2.25 2.25 0 002.25 2.25z" />
            </svg>
          </div>
          <span className="text-sm font-medium">กล้องจะแสดงที่นี่</span>
          <span className="badge badge-ghost badge-sm">On-device Processing (PDPA)</span>
        </div>
      </div>
    </div>
  );
}
