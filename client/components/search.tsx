'use client';
import { useState } from "react";

export default function Search() {
  const [keyword, setKeyword] = useState("");
  const [location, setLocation] = useState("");
  const [datePosted, setDatePosted] = useState("Anytime");
  const [experience, setExperience] = useState("All levels");
  const [jobType, setJobType] = useState("Any");

  return (
    <div className="mt-6 bg-white rounded-lg p-4 shadow-sm border border-gray-200 ">

      {/* First row: main search input */}
      <div className="flex gap-3">
        <input
          type="text"
          placeholder="Enter Job Type or Title"
          className="flex-1 border border-gray-300 rounded-md px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
        />
      </div>

      {/* Second row: filters */}
      <div className="mt-4 flex flex-wrap gap-3">
        {/* Location */}
        <input
          type="text"
          placeholder="Location"
          className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />

        {/* Date Posted */}
        <select
          className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
          value={datePosted}
          onChange={(e) => setDatePosted(e.target.value)}
        >
          <option>Anytime</option>
          <option>Last 24 hours</option>
          <option>Last 3 days</option>
          <option>Last 7 days</option>
          <option>Last 14 days</option>
        </select>

        {/* Experience Level */}
        <select
          className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
          value={experience}
          onChange={(e) => setExperience(e.target.value)}
        >
        <option value="" disabled>Experience Level</option>
          <option>All levels</option>
          <option>Entry level</option>
          <option>Mid level</option>
          <option>Senior level</option>
        </select>

        {/* Job Type */}
        <select
          className="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
          value={jobType}
          onChange={(e) => setJobType(e.target.value)}
        >
          <option>Any</option>
          <option>Full-time</option>
          <option>Part-time</option>
          <option>Contract</option>
          <option>Internship</option>
        </select>

        {/* Search Button */}
        <button className="bg-indigo-600 text-white px-5 py-2 rounded-md hover:bg-indigo-700 transition font-medium">
          Search
        </button>
      </div>
    </div>
  );
}
