import {cookies} from "next/headers"
export default async function JobDetailPage({params}){
    const {jobId}=await params
    const cookieStore= await cookies()
        const accessTokenCookie = cookieStore.get("access_token"); 
          const cookieHeader = accessTokenCookie
        ? `access_token=${accessTokenCookie.value}`
        : "";
    const res = await fetch(
    `http://localhost:8000/job/${encodeURIComponent(jobId)}`,
    {
      cache: "no-store", 
       headers:{
            Cookie:cookieHeader
        }
    }
  );

  if (!res.ok) {
    throw new Error("Failed to fetch job");
  }

  const data = await res.json();
  const job= data.data[0];
    return (
       <div className="bg-gray-100 min-h-screen">
      <div className="px-6 py-10 grid grid-cols-1 lg:grid-cols-3 gap-8">

        {/* MAIN CONTENT */}
        <div className="lg:col-span-2 space-y-8">

          {/* Header */}
          <div className="bg-white rounded-2xl p-8 shadow-sm">
            <h1 className="text-3xl font-bold text-gray-900">
              {job.job_title}
            </h1>
            <p className="mt-2 text-gray-600 text-lg">
              {job.employer_name}
            </p>

            <div className="flex flex-wrap gap-4 mt-4 text-sm text-gray-600">
              <span>📍 {job.job_location}</span>
              <span>💼 {job.job_employment_type}</span>
              <span>🕒 {job.job_posted_at}</span>
            </div>
          </div>

          {/* Description */}
          <section className="bg-white rounded-2xl p-8 shadow-sm">
            <h2 className="text-2xl font-semibold mb-4">Job Description</h2>
            <p className="text-gray-700 whitespace-pre-line">
              {job.job_description}
            </p>
          </section>

          {/* Responsibilities */}
          {job.job_highlights?.Responsibilities && (
            <section className="bg-white rounded-2xl p-8 shadow-sm">
              <h2 className="text-xl font-semibold mb-4">Responsibilities</h2>
              <ul className="list-disc pl-6 space-y-2 text-gray-700">
                {job.job_highlights.Responsibilities.map(
                  (item: string, i: number) => (
                    <li key={i}>{item}</li>
                  )
                )}
              </ul>
            </section>
          )}

          {/* Qualifications */}
          {job.job_highlights?.Qualifications && (
            <section className="bg-white rounded-2xl p-8 shadow-sm">
              <h2 className="text-xl font-semibold mb-4">Qualifications</h2>
              <ul className="list-disc pl-6 space-y-2 text-gray-700">
                {job.job_highlights.Qualifications.map(
                  (item: string, i: number) => (
                    <li key={i}>{item}</li>
                  )
                )}
              </ul>
            </section>
          )}
        </div>

        {/* APPLY SIDEBAR */}
        {/* <aside className="space-y-6"> */}
         <div className="space-y-6">
          <div className="bg-white rounded-2xl p-6 shadow-sm sticky top-6">
            <h3 className="text-lg font-semibold mb-4">
              Apply for this role
            </h3>

            <a
              href={job.job_apply_link}
              target="_blank"
              className="block w-full text-center bg-indigo-600 text-white font-semibold py-3 rounded-xl hover:bg-indigo-700 transition"
            >
              Apply Now
            </a>

            <p className="text-xs text-gray-600 text-center mt-3">
              External application
            </p>
          </div>

          {/* Benefits */}
          {job.job_highlights?.Benefits && (
            <div className="bg-white rounded-2xl p-6 shadow-sm">
              <h3 className="text-lg font-semibold mb-3">Benefits</h3>
              <ul className="space-y-2 text-sm text-gray-700">
                {job.job_highlights.Benefits.map(
                  (benefit: string, i: number) => (
                    <li key={i}>✔ {benefit}</li>
                  )
                )}
              </ul>
            </div>
          )}

          {/* Employer Reviews */}
          {job.employer_reviews && (
            <div className="bg-white rounded-2xl p-6 shadow-sm">
              <h3 className="text-lg font-semibold mb-3">
                Employer Reviews
              </h3>

              {job.employer_reviews.map((review: any, i: number) => (
                <div key={i} className="mb-3">
                  <p className="text-sm font-medium">
                    {review.publisher}
                  </p>
                  <p className="text-xs text-gray-600">
                    ⭐ {review.score} / {review.max_score} ({review.review_count})
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
    )
}