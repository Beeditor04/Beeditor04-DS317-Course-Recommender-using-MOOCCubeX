import { useEffect, useLayoutEffect, useState } from "react";
import { useLocation } from "react-router-dom";

// Components, pages
import Sidebar from "../components/Sidebar";
import Card from "../components/Card";
import "./Home.css";

// Sample data
import recommend_data from "../sample/recommend.json";
import courses_data from "../sample/courses.json";
import users_data from "../sample/users.json";


const Home = () => {
  const location = useLocation();
  const { user } = location.state || { user: "Guest" }; // Default to "Guest" if no user is passed
  const [showAll, setShowAll] = useState(false);

  const handleShowAll = () => {
    setShowAll(!showAll);
  };
  return (
    <div className="wrapper flex flex-row h-screen">
      <Sidebar />
      <div className="container w-full overflow-y-auto h-screen">
        <h1 className="text-4xl text-left m-10">
          Hello {user}, wanna try something spicy?
        </h1>
        <div className="recommend w-full">
        <div className="cards grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-x-10 gap-y-10 px-10 justify-center items-center">
          {recommend_data.slice(0, showAll ? recommend_data.length : 4).map((recommend) => (
            <Card key={recommend.id} radius={"30rem"} className="recommend-item w-full h-40 flex justify-center items-center content-center">
              <p>{recommend.id}</p>
              <p>{recommend.name}</p>
             </Card>
          ))}
        </div> 
        <a onClick={handleShowAll} className="btn-text text-right w-full block pr-10">
            {showAll ? "Show less" : "Show all"}
          </a>
        </div>
        
        <div className="courses">
          {/* {courses_data} */}
        </div>
      </div>
    </div>
  );
};

export default Home;
