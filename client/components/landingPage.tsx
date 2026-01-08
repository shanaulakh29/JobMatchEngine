import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-white">
      {/* Navbar */}
      <header className="flex items-center justify-between px-8 py-6">
        <h1 className="text-2xl font-bold text-indigo-600">JobMatch</h1>
        <div className="flex gap-4">
          <Link
            href="/login"
            className="border border-gray-300 px-4 py-2 rounded-lg text-lg font-semibold text-gray-700 hover:bg-gray-100 transition"
          >
            Login
          </Link>
          <Link
            href="/signup"
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg shadow hover:bg-indigo-700 transition"
          >
            Sign Up
          </Link>
        </div>
      </header>

      <main className="px-8 md:px-16 mt-16 grid md:grid-cols-2 gap-12 items-center">
        {/* Left */}
        <div>
          <h2 className="text-4xl md:text-5xl font-extrabold text-gray-900 leading-tight">
            Find Jobs That <span className="text-indigo-600">Match Your Resume</span>
          </h2>

          <p className="mt-6 text-lg text-gray-600 max-w-xl">
            Upload your resume and instantly discover personalized job
            opportunities tailored to your skills, experience, and career goals.
            No more endless searching.
          </p>

          <div className="mt-8 flex gap-4">
            <Link
              href="/signup"
              className="bg-indigo-600 text-white px-6 py-3 rounded-lg text-lg font-semibold shadow hover:bg-indigo-700 transition"
            >
              Get Started
            </Link>

            <Link
              href="/login"
              className="border border-gray-300 px-6 py-3 rounded-lg text-lg font-semibold text-gray-700 hover:bg-gray-100 transition"
            >
              Login
            </Link>
          </div>
        </div>

        {/* Right */}
        <div className="">
          <div className="bg-white rounded-2xl shadow-xl p-6 space-y-4 m-6">
            <h3 className="text-lg font-semibold text-gray-900">
              🔍 Resume-Based Job Matching
            </h3>
            <p className="text-gray-600 text-sm">
              Our engine analyzes your resume and matches it with the latest
              job listings across multiple platforms.
            </p>

            <div className="border-t pt-4">
              <p className="text-sm text-gray-500">
                ✓ AI-powered matching <br />
                ✓ Real-time job listings <br />
                ✓ Personalized recommendations
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Features */}
      <section className="mt-24 px-8 md:px-16">
        <h3 className="text-3xl font-bold text-gray-900 text-center">
          Why JobMatch?
        </h3>

        <div className="mt-12 grid md:grid-cols-3 gap-8">
          <Feature
            title="Smart Resume Parsing"
            description="We understand your resume — skills, experience, and roles — not just keywords."
          />
          <Feature
            title="Latest Job Listings"
            description="Fetch real-time job opportunities from trusted platforms."
          />
          <Feature
            title="Personalized Results"
            description="Jobs ranked based on how well they match YOU."
          />
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-24 py-8 text-center text-gray-500 text-sm">
        © {new Date().getFullYear()} JobMatch. Built to simplify job searching.
      </footer>
    </div>
  );
}

function Feature({
  title,
  description,
}: {
  title: string;
  description: string;
}) {
  return (
    <div className="bg-white rounded-xl shadow p-6 hover:shadow-lg transition">
      <h4 className="text-lg font-semibold text-gray-900">{title}</h4>
      <p className="mt-2 text-gray-600 text-sm">{description}</p>
    </div>
  );
}
