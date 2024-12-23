// import { Link } from "react-router-dom";
import { Link, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import Card from "../components/Card";
import axios from "../api/axios";

import "./Sidebar.css";

// sample data
import users_data from "../sample/users.json";
import courses_data from "../sample/courses.json";
import SidebarIcon from "../assets/sidebar_icon.svg";
import UserIcon from "../assets/user.svg";

const Sidebar = ({ id }) => {
  const [collapse, setCollapse] = useState(false);
  const [users_data, setUsersData] = useState([]);
  
  const handleCollapse = () => {
    setCollapse(!collapse);
  }
  
  // request user info api
  useEffect(() => {
    const requestUser = async () => {
      try {
        console.log("------HERE!!!!");
        const response = await axios.get(`/users/${id}`,
          {
            headers: {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Headers': 'Content-Type, Authorization',
              }
          }
        );
        console.log("Response: ", response);
        setUsersData(response.data);
      } catch (error) {
        console.log("Error: ", error);
      }
    };
    requestUser();
  }, []);

  return (
    <div className={`cards sidenav ${collapse ? "collapsed" : ""}`} style={{width: collapse ? "0" : "30%"}}>
      <Card className="w-full min-h-full" radius="0px">
        <div className="side-header flex flex-row justify-between gap-3">
          <h1 className="text-xl">User information</h1>
          <img 
            src={SidebarIcon} 
            alt="Collapse" 
            onClick={handleCollapse} 
            className="btn-collapse" 
            style={{ cursor: 'pointer' }}
          />        
        </div>
        <img
          src={UserIcon}
          alt="avatar"
          className="user-icon w-14 mx-auto pt-[5rem] pb-10"
        />
        <div className="side-body flex flex-col items-center">
          <p className="text-center pb-1"><b className="text-purple-300">Name:</b> {users_data.name}</p>
          <Card className="w-auto h-auto" color="#141e3b">
            <ul className="pl-3">
              <li><b className="text-purple-300">Id:</b> {users_data.id}</li>
              <li className="flex list-disc flex-row gap-2 flex-wrap max-w-full"><b className="text-purple-300">Registerd:</b> 
              {users_data.courses.map((c) => (
                <Link to={`/details/${c}`} state={{course : courses_data.find(course => course.id === c)}}><p className="status-yes">{c}</p></Link>
              ))}
              </li>
            </ul>
          </Card>

        </div>
      </Card>
    </div>
  );
};

export default Sidebar;
