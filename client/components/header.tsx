'use client'
import { useRouter } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
export default function Header(){
    const router=useRouter()
    function handleLogout(){
        router.push("/")
    }
    return (
<header className="w-full">
      <div className="  flex items-center justify-between  py-4 md:py-5">
        {/* Left section */}
        <div className="flex items-center gap-6 md:gap-10">
          {/* Logo */}
          <Link href="/">
            <div className="flex items-center gap-2 cursor-pointer hover:scale-105 transition-transform duration-200">
              <Image
                src="/jobmatchicon.png"
                alt="JobMatch Logo"
                width={40}
                height={40}
                className="rounded-full"
              />
              <h1 className="text-xl md:text-2xl font-bold text-indigo-600 tracking-tight">
                JobMatch
              </h1>
            </div>
          </Link>

          {/* Navigation */}
          <ul className="flex items-center gap-8 text-sm md:text-lg font-medium text-gray-600">
            <li className="cursor-pointer hover:text-indigo-600 transition-colors duration-200">
              <Link href="/home">Home</Link>
            </li>
            <li className="cursor-pointer hover:text-indigo-600 transition-colors duration-200">
              <Link href="/applied-jobs">Applied Jobs</Link>
            </li>
          </ul>
        </div>

        {/* Right section */}
        <div className="flex items-center gap-4">
          <button
            onClick={handleLogout}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-2 py-1 md:px-4 md:py-2 rounded-2xl shadow-md transition-all duration-200"
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}