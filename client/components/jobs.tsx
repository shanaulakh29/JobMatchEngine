import {cookies} from "next/headers"
import { redirect } from "next/navigation";
import JobCard from "./jobCard";
export default async function Jobs(){
    const cookieStore= await cookies()
    const accessTokenCookie = cookieStore.get("access_token"); 
      const cookieHeader = accessTokenCookie
    ? `access_token=${accessTokenCookie.value}`
    : "";
    const res=await fetch("http://localhost:8000/job/jobs",{
        cache:"no-store",
        headers:{
            Cookie:cookieHeader
        }
    })
    console.log("STATUS IS ",res.status)
    if(res.status===401){
        redirect("/login")
    }
    else if (!res.ok) {
        const text = await res.text();
        throw new Error(`Failed to fetch jobs: ${text}`);
    }

    const result = await res.json();
    const jobs=result.data


    return(
       <div className="mt-6">
      <h2 className="text-4xl mb-6">Recommended Jobs</h2> 
      <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        {jobs.map((job) => (
          <JobCard key={job.job_id} job={job} />
        ))}
      </div>
    </div>
    )
}