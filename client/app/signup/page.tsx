"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function SignupPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [occupation, setOccupation] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);
    formData.append("email", email);
    formData.append("occupation", occupation);
    
    try {
    const res = await fetch("http://localhost:8000/auth/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData.toString(),
    });

    if (!res.ok) {
      const error = await res.json();
      throw new Error(error.detail || "Signup failed");
    }

    router.push("/login");
  } catch (err: any) {
    alert(err.message || "Network error");
  }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-md w-full  bg-white rounded-2xl shadow-xl p-10 space-y-10">
        
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-indigo-700 mb-2">
            Create Account
          </h1>
          <p className="text-gray-500">
            Join JobMatch and discover jobs tailored to you
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSignup} className="space-y-4">

            {/* Username */}
          <div className="flex flex-col">
            <label className="text-sm text-gray-700 mb-1">
              Username
            </label>
            <input
              type="text"
              placeholder="john123"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
              required
            />
          </div>

          {/* Email */}
          <div className="flex flex-col">
            <label className="text-sm  text-gray-700 mb-1">
              Email
            </label>
            <input
              type="email"
              placeholder="john@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
              required
            />
          </div>

          {/* Occupation */}
          <div className="flex flex-col">
            <label className="text-sm text-gray-700 mb-1">
              Occupation
            </label>
            <input
              type="text"
              placeholder="Software Engineer"
              value={occupation}
              onChange={(e) => setOccupation(e.target.value)}
              className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
            />
          </div>

          

          {/* Password */}
          <div className="flex flex-col">
            <label className="text-sm  text-gray-700 mb-1">
              Password
            </label>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 outline-none"
              required
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            className="w-full bg-indigo-600 text-white font-semibold py-2 rounded-lg shadow hover:bg-indigo-700 transition"
          >
            Create Account
          </button>
        </form>

        {/* Footer */}
        <p className="text-center text-gray-500 text-sm">
          Already have an account?{" "}
          <Link href="/login" className="text-indigo-600 font-medium hover:underline">
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
}
