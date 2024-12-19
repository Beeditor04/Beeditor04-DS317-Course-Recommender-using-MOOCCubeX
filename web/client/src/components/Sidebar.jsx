// import { Link } from "react-router-dom";
import { Link, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import Card from "../components/Card";
import "./Sidebar.css";

const Sidebar = () => {
  return (
  <div className="cards sidenav">
    <Card className="w-full h-full">
      Contents
    </Card>
    </div>
  )
};

export default Sidebar;
