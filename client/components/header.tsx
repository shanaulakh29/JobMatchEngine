import Image from "next/image";
export default function Header(){
    return (
    <header className="w-full border-b bg-white">
      <div className="flex   items-center justify-between px-6 py-4">
        
        {/* Left section */}
        <div className="flex items-center gap-5 md:gap-10">
            <div className="flex items-center">
            <Image src="/jobmatchicon.png" alt="job match icon" width={40}
              height={40}/>
            <h1 className="text-sm md:text-2xl font-semibold tracking-tight text-gray-900">
            JobMatch
          </h1>
            </div>
         

          <ul className="flex items-center gap-8 text-sm md:text-lg font-medium text-gray-600">
            <li className="cursor-pointer hover:text-gray-900 transition">
              Jobs
            </li>
            <li className="cursor-pointer hover:text-gray-900 transition">
              My Resumes
            </li>
            <li className="cursor-pointer hover:text-gray-900 transition">
              Applied Jobs
            </li>
          </ul>
        </div>

        {/* Right section */}
        <div className="flex items-center ml-4 ">
          <div className="h-10 w-10 rounded-full border border-gray-200 overflow-hidden hover:ring-2 hover:ring-gray-300 transition cursor-pointer">
            <Image
              src="/settings.png"
              alt="User profile"
              width={40}
              height={40}
            />
          </div>
        </div>
      </div>
    </header>
  );
}