import { useEffect, useState } from "react";
import { useLocation, useParams, Link } from "react-router-dom";

const Details = () => {
  const location = useLocation();
  console.log(location.state);
  const { course } = location.state || {};
  return (
    <>
    <h1 className="text-4xl text-center m-10">{course.id}: {course.name}</h1>
    <div className="details-container flex flex-col items-center justify-center w-2/3 mx-auto gap-5">
    <div className="card container mx-auto p-5">
      <p className="flex flex-row gap-1"><t className="text-purple-300 font-bold">Field:</t> {course.field.map((f) => (
        <p className="status-waiting w-auto">{f}</p>
      ))}</p>
      <p><t className="text-purple-300 font-bold">Prerequisities:</t> {course.prerequisites || "None"}</p>
      <p><t className="text-purple-300 font-bold">About:</t> {course.about}</p>
      <p><t className="text-purple-300 font-bold">School:</t></p>
      <p><t className="text-purple-300 font-bold">Teacher:</t></p>
      <p><t className="text-purple-300 font-bold">Resources:</t></p>
    </div>
    <Link class="btn-secondary px-3 py-2" to="/home">
        Back to Home
      </Link>
    </div>
    </>
  );
};

export default Details;
