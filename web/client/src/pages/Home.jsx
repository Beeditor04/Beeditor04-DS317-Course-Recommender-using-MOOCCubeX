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
  const [showAllRec, setShowAllRec] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [recommend_data, setRecommendData] = useState([]);
  const [detailedCourses, setDetailedCourses] = useState(recommend_data_sample);

  const [user, setUser] = useState({ id: "U_24", name: "Guest", course: [] });
  const [courses_data, setCoursesData] = useState([]);
  const [courses_data_full, setCoursesDataFull] = useState([]);
  const [success, setSuccess] = useState(true);
 
  const num_of_rows = 10;
  const [showMore, setShowMore] = useState(num_of_rows);
  
  const handleShowMore = () => {
    setShowMore(showMore + 20);
  };
  const handleShowLess = () => {
    setShowMore(showMore - 20);
  }

  const storedUser = JSON.parse(localStorage.getItem('user'));
  const handleShowAllRec = () => {
    setShowAllRec(!showAllRec);
  };

  // update user info
  useEffect(() => {
    const requestUser = async () => {
      try {
        const response = await axios.get(`/user/${storedUser.id || location.state.id}`);
        setUser(response.data);
      } catch (err) {
        console.error("Error fetching user:", err);
      }
    }
    requestUser();
  }, []);


  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };
  
  const filteredCourses = courses_data_full.filter((course) => {
    const name = course.name || "";
    const id = course.id || "";
    const prerequisites = course.prerequisites || "";
    const query = searchQuery.toLowerCase();
    return (
      name.toLowerCase().includes(query) ||
      id.toLowerCase().includes(query) ||
      prerequisites.toLowerCase().includes(query)
    );
  });
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
}, [user.id]);

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

// list of courses
useEffect(() => {
  const fetchAllCourses = async () => {
    try {
      const response = await axios.get("/all_course");
      setCoursesData(response.data); // e.g., ["C_1017355", "C_1017419", "C_1025064"]
    } catch (err) {
      console.error("Error fetching all courses:", err);
    }
  };
  fetchAllCourses();
}, []);

useEffect(() => {
  const fetchAllCoursesFull = async () => {
    const tempCourses = [];
    try {
      for (const id of courses_data.slice(0, showMore)) {
        const response = await axios.get(`/course/${id}`);
        tempCourses.push(response.data);
        console.log("Courses data SUCCESSED!!!:", response.data);
      }
      setCoursesDataFull(tempCourses); // e.g., ["C_1017355", "C_1017419", "C_1025064"]
    } catch (err) {
      console.error("Error fetching all courses:", err);
    }
  };
  fetchAllCoursesFull();
}, [courses_data, showMore]);

  return (
    <div className="wrapper flex flex-row h-screen">
      {/*---Sidebar---*/}
      <Sidebar users_data={user}/>
      {/*---Recommend---*/}
      <div className="wrapper-container w-full overflow-y-auto h-screen">
      <div className="recommend-container w-full overflow-y-auto h-auto mb-10">
        <h2 className="text-3xl text-left m-10">
          Hello {user.name}, wanna try something new?
        </h2>
        { 
        !success ? (<div>Waiting</div>) : ( 
          <div className="recommend-course w-full">
          <div className="cards grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-x-10 gap-y-3 xl:gap-y-10 px-10 justify-center items-center">
            {detailedCourses
              .slice(0, showAllRec ? detailedCourses.length : 4)
              .map((recommend) => (
                <Link 
                  to={`/details/${recommend.id}`} 
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
            onClick={handleShowAllRec}
            className="btn-text text-right w-full block pr-10"
          >
            {showAllRec ? "Show less" : "Show all"}
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
          
          <CourseTable courses_data={filteredCourses} length={showMore} user_course={user.course} user_id={user.id}/>
        </div>
        <div className="show-more flex flex-row justify-end">
        {showMore > num_of_rows && (
          <a
            onClick={handleShowLess}
            className="btn-text text-right block pr-10"
          >
            Show Less
          </a>
        )}
        <a
            onClick={handleShowMore}
            className="btn-text text-right block pr-10"
          >
            Show more
          </a>
      </div>
      </div>
      </div>

    </div>
  );
};

export default Home;
