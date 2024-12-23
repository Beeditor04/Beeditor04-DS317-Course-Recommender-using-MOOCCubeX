import { useEffect, useState } from "react";
import { useLocation, useParams, Link } from "react-router-dom";
import axios from "../api/axios";

const Details = () => {
  const location = useLocation();
  const [course, setCourse] = useState({
    id: "C_1017355",
    name: "Not Found",
    prerequisites: "Prerequisites",
    field: ["Field1", "Field2"],
    about: "About",
    school_name: "School Name",
    teacher_name: "Teacher Name",
    resource: ["Resource1", "Resource2"],
  }
  );

  console.log("Detail location:", location.state);
  const id = location.state.course || "U_3179";
  useEffect(() => {
    const fetchAllCourses = async () => {
      try {
        const response = await axios.get(`/course/${id}`, {
          headers: {"Access-Control-Allow-Origin": "*"}
        });
        console.log("useEffect called with id:", id);
        console.log("Courses data SUCCESSED!!!:", response.data);
        if (response.data.length === 0) {
          console.log("No course found with id:", id);
          return;
        }
        setCourse(response.data); // e.g., ["C_1017355", "C_1017419", "C_1025064"]
      } catch (err) {
        console.error("Error fetching all courses:", err);
      }
    };
    fetchAllCourses();
  }, [location]);
  
  console.log(course);
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
      <p><t className="text-purple-300 font-bold">School:</t>{course.school_name}</p>
      <p><t className="text-purple-300 font-bold">Teacher:</t>{course.teacher_name}</p>
      <p><t className=" text-purple-300 font-bold">Resources:</t>{course.resource.map((r) => (
        <p className="w-auto">{r.title} {r.resource_id} {r.chapter}</p>
      ))}
      </p>
    </div>
    <Link class="btn-secondary px-3 py-2" to="/home">
        Back to Home
      </Link>
    </div>
    </>
  );
};

export default Details;
