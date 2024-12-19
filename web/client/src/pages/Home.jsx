import { useEffect, useLayoutEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import "./Home.css";

const Home = () => {
  const location = useLocation();
  const { user } = location.state || { user: "Guest" }; // Default to "Guest" if no user is passed
  return (
    <div className="wrapper flex flex-row h-screen">
      <Sidebar />
      <div className="container w-full overflow-y-auto h-screen">
        <h1 className="text-4xl text-center m-10">
          Hello {user}, Welcome to Summoner's Rift
        </h1>
        <div className="recommend">

        </div> 
        <div classname="courses">
          
        </div>
      </div>
    </div>
  );
};

export default Home;
