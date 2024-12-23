import React, { useState, useEffect, useInsertionEffect } from "react";
import { Link, useLocation } from "react-router-dom";

// Components, pages
import Sidebar from "../components/Sidebar";
import Card from "../components/Card";
import CourseTable from "../components/CourseTable";
import axios from "../api/axios";
import "./Home.css";

// Sample data
import recommend_data_sample from "../sample/recommend.json";
// import courses_data from "../sample/courses.json";

const Home = () => {
  const location = useLocation();
  const [showAll, setShowAll] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [courses_data, setCoursesData] = useState([]);
  const [recommend_data, setRecommendData] = useState([]);
  const [detailedCourses, setDetailedCourses] = useState([]);
  const [success, setSuccess] = useState(false);

  const storedUser = JSON.parse(localStorage.getItem('user'));
  const user = location.state || storedUser || { id: "U_1", name: "Guest", course: [] };
  console.log(user);
  const handleShowAll = () => {
    setShowAll(!showAll);
  };

  useEffect(() => {
    if (location.state) {
      localStorage.setItem('user', JSON.stringify(location.state));
    }
  }, [location.state]);

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };
  
  const filteredCourses = courses_data.filter(course =>
    // course.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    // course.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    // course.prerequisites.toLowerCase().includes(searchQuery.toLowerCase())
    course.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // request api
  useEffect(() => {
  const fetchAllRecommend = async () => {
    try {
      const response = await axios.get("/rec/" + user.id);
      console.log("Recommend data SUCCESSED!!!:", response.data);
      setRecommendData(response.data); // e.g., ["C_1017355", "C_1017419", "C_1025064"]
    } catch (err) {
      console.error("Error fetching all recommend:", err);
    }
  };
  fetchAllRecommend();
}, []);

useEffect(() => {
  const fetchCourseDetails = async () => {
    const tempCourses = [];
    for (const id of recommend_data) {
      try {
        const response = await axios.get(`/course/${id}`);
        if (response.data) {
          tempCourses.push(response.data);
        }
        console.log("Recommend data-details SUCCESSED!!!:", response.data);
        setSuccess(true);
      } catch (err) {
        console.error(`Error fetching course ${id}:`, err);
      }
    }
    setDetailedCourses(tempCourses);
  };

  if (recommend_data.length > 0) {
    fetchCourseDetails();
  }
}, [recommend_data]);

useEffect(() => {
  const fetchAllCourses = async () => {
    try {
      const response = await axios.get("/all_course");
      console.log("Courses data SUCCESSED!!!:", response.data);
      setCoursesData(response.data); // e.g., ["C_1017355", "C_1017419", "C_1025064"]
    } catch (err) {
      console.error("Error fetching all courses:", err);
    }
  };
  fetchAllCourses();
}, []);

  return (
    <div className="wrapper flex flex-row h-screen">
      {/*---Sidebar---*/}
      <Sidebar users_data={user}/>
      {/*---Recommend---*/}
      <div className="wrapper-container w-full overflow-y-auto h-screen">
      <div className="recommend-container w-full overflow-y-auto h-auto mb-10">
        <h2 className="text-3xl text-left m-10">
          Hello {user.name}, wanna try something spicy?
        </h2>
        { 
        !success ? (<div>Waiting</div>) : ( 
          <div className="recommend-course w-full">
          <div className="cards grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-x-10 gap-y-3 xl:gap-y-10 px-10 justify-center items-center">
            {detailedCourses
              .slice(0, showAll ? detailedCourses.length : 4)
              .map((recommend) => (
                <Link
                  to={{ pathname: `/details/${recommend.id}` }}
                  state={{ course: recommend }}
                  key={recommend.id}
                  className="w-full h-28 xl:h-40"
                >
                  <Card
                    radius={"20rem"}
                    className="recommend-item w-full h-full flex justify-center items-center content-center"
                  >
                    <p style={{ color: "var(--neutral-200)" }}>
                      {recommend.id}
                    </p>
                    <p className="text-center">{recommend.name}</p>
                  </Card>
                </Link>
              
              ))}
          </div>
          <a
            onClick={handleShowAll}
            className="btn-text text-right w-full block pr-10"
          >
            {showAll ? "Show less" : "Show all"}
          </a>
        </div>
        )}
      </div>
      {/*---All available Courses---*/}
      <div className="courses-container w-full overflow-y-auto h-auto p-10">
        <div className="table-wrapper w-auto h-auto overflow-y-hidden">
          <div className="courses-header flex flex-row gap-5 p-5">
            <h1 className="text-3xl mb-5">Courses</h1>
            <div className="search-bar">
              <input
                type="text"
                placeholder="Search courses..."
                value={searchQuery}
                onChange={handleSearchChange}
                className="input-field w-auto "
              />
            </div>
          </div>
          
          <CourseTable courses_data={filteredCourses} />
        </div>
      </div>
      </div>

    </div>
  );
};

export default Home;
