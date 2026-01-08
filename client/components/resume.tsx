'use client';
import Image from "next/image";
import { useState } from "react";

export default function Resume() {
  const [resume, setResume] = useState(null);

  return (
    <div className="max-w-sm rounded-xl border border-gray-200 bg-white p-5 shadow-sm hover:shadow-lg transition-all duration-200">
      
      {/* Top section */}
      <div className="flex items-center gap-4">
        <div className="flex h-11 w-11 items-center justify-center rounded-lg bg-indigo-50">
          <Image
            src="/document.png"
            alt="document image"
            width={24}
            height={24}
          />
        </div>

        <div>
          <p className=" font-semibold text-gray-900">
            Software Developer Resume
          </p>
          <p className="text-xs text-gray-500">
            Uploaded Jan 14, 2025
          </p>
        </div>
      </div>

      {/* Skills */}
      <div className="mt-4 flex flex-wrap gap-2">
        <span className="rounded-full bg-indigo-50 px-3 py-1 text-xs font-medium text-indigo-700">
          React
        </span>
        <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
          Node.js
        </span>
        <span className="rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-700">
          TypeScript
        </span>
      </div>

    </div>
  );
}
