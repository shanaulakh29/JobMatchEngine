import Image from "next/image";
import Header from "../../components/header"
import AllResumes from "../../components/allResumes"
import Search from "../../components/search"
import Jobs from "../../components/jobs"
import Login from "../../components/login"
export default function Home() {
  return (
    <div className="px-6">
      <Header/>
      <div>
        <h1 className="text-black text-3xl md:text-5xl mt-10">Discover your Next Opportunity</h1>
        <p className="text-black text-2xl md:text-3xl mt-2">Select a resume to get personalized job matches based on your skills and experience</p>
      </div>
      
      <div className="mt-10">
        <h2 className="text-4xl mb-6">Select a Resume</h2>
        <AllResumes/>
      </div>

      <Search/>

      <Jobs/>
      </div>


  );
}
