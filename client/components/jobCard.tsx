"use client"
import { useRouter } from "next/navigation";
export default function JobCard({job}){
    const router=useRouter();
    function handleClick(){
        router.push("")
    }
    return (
       <div
      onClick={handleClick}
      className="cursor-pointer flex flex-col justify-between p-5 bg-white border border-gray-200 rounded-xl shadow-md hover:shadow-xl transition-shadow duration-200 hover:scale-[1.02] transform"
    >
      {/* Logo + Title */}
      <div className="flex gap-4">
        <div className="flex items-center justify-center w-16 h-16 rounded-lg bg-gray-100 overflow-hidden">
          {job.employer_logo ? (
            <img
              src={job.employer_logo}
              alt={job.employer_name}
              className="w-full h-full object-contain"
            />
          ) : (
            <span className="text-xl font-bold text-gray-500">
              {job.employer_name.charAt(0)}
            </span>
          )}
        </div>

        <div className="flex-1 flex flex-col">
          <h2 className="text-lg font-semibold text-gray-900">{job.job_title}</h2>
          <p className="text-sm text-gray-700">{job.employer_name}</p>
          <p className="mt-1 text-xs text-gray-500">
            {job.job_location} · {job.job_employment_type}
          </p>
        </div>
      </div>

      {/* Badges */}
      <div className="mt-3 flex flex-wrap gap-2">
        {job.job_is_remote ? (
          <span className="px-2 py-1 bg-indigo-50 text-indigo-700 text-xs font-medium rounded-full">
            Remote
          </span>
        ) : (
          <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs font-medium rounded-full">
            On-site
          </span>
        )}

        <span className="px-2 py-1 bg-gray-100 text-gray-500 text-xs font-medium rounded-full">
          {job.job_employment_type}
        </span>
      </div>

      {/* Description snippet */}
      <p className="mt-3 text-sm text-gray-600 line-clamp-3">
        {job.job_description}
      </p>

      {/* Footer: Posted date */}
      <div className="mt-4 text-xs text-gray-400 flex justify-between items-center">
        <span>{job.job_posted_at}</span>
        <span className="text-indigo-600 font-medium">View Details →</span>
      </div>
    </div>
    )
}