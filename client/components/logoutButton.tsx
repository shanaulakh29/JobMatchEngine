"use client";

import { useRouter } from "next/navigation";

export default function LogoutButton() {
  const router = useRouter();

  async function handleLogout() {
    try {
      const res = await fetch("http://localhost:8000/auth/logout", {
        method: "POST",
        credentials: "include",
      });

      if (res.ok) {
        router.push("/");
      } else {
        const data = await res.json();
        alert(data.message ?? "Logout failed");
      }
    } catch (err) {
      console.error(err);
      alert("Network error");
    }
  }

  return (
    <button
      onClick={handleLogout}
      className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-2 py-1 md:px-4 md:py-2 rounded-2xl shadow-md transition-all"
    >
      Logout
    </button>
  );
}
