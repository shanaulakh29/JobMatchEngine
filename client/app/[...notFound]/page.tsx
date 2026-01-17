"use client"; // client component if you want interactivity

import Link from "next/link";

export default function NotFoundPage() {
  return (
    <div className="min-h-screen flex flex-col justify-center items-center px-4">
      <h1 className="text-8xl font-extrabold mb-6">404</h1>
      <p className="text-2xl md:text-3xl mb-4 text-center">
        Oops! The page you are looking for does not exist.
      </p>
      <p className="mb-8 text-center opacity-80">
        Maybe you mistyped the URL or the page has been moved.
      </p>
      <Link
        href="/"
        className="bg-indigo-500 text-white font-semibold px-6 py-3 rounded-lg shadow-lg hover:bg-indigo-700 transition"
      >
        Go Back Home
      </Link>
    </div>
  );
}
