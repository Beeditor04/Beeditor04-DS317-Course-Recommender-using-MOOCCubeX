import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";

// Components, pages
import Sidebar from "../components/Sidebar";
import Card from "../components/Card";
import CourseTable from "../components/CourseTable";
import "./Home.css";

// Sample data
import recommend_data from "../sample/recommend.json";
import courses_data from "../sample/courses.json";

const Home = () => {
  const location = useLocation();
  const { user } = location.state || { user: "Guest" }; // Default to "Guest" if no user is passed
  const [showAll, setShowAll] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleShowAll = () => {
    setShowAll(!showAll);
  };

  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };
  
  const filteredCourses = courses_data.filter(course =>
    course.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    course.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
    course.prerequisites.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // request api
  
  return (
    <div className="wrapper flex flex-row h-screen">
      {/*---Sidebar---*/}
      <Sidebar id={user}/>
      {/*---Recommend---*/}
      <div className="wrapper-container w-full overflow-y-auto h-screen">
      <div className="recommend-container w-full overflow-y-auto h-auto mb-10">
        <h2 className="text-3xl text-left m-10">
          Hello {user}, wanna try something spicy?
        </h2>
        <div className="recommend-course w-full">
          <div className="cards grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-x-10 gap-y-3 xl:gap-y-10 px-10 justify-center items-center">
            {recommend_data
              .slice(0, showAll ? recommend_data.length : 4)
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
