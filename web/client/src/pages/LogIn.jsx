import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axios";

import UserIcon from "../assets/user.svg";
import Card from "../components/Card";
import "./LogIn.css";
const LogIn = () => {
  const USER_REGEX = /^U_\d+$/;

  const [user, setUser] = useState("");
  const [validUser, setValidUser] = useState(false);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    setValidUser(USER_REGEX.test(user));
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("User: ", user);
    try {
      const res = await axios.get(`/user/${user}`, {
        headers: {"Access-Control-Allow-Origin": "*"}
      }
      );
      console.log("Response: ", res);
      if (validUser) {
        setSuccess(true);
        navigate("/home", { state:  res.data  });
      }
      console.log("Success?: ", success);
    } catch (error) {
      console.log("Error: ", error);
    }
  };

  // const [userFocus, setUserFocus] = useState(false);
  return (
    <>
      <div className="cards flex items-center justify-center h-screen">
        {/* <div className="container mx-auto card w-1/3 h-1/2"> */}
        <Card className="mx-auto w-[27rem] h-1/2">
          <h1 className="text-4xl text-center my-10 title-color">Log In</h1>
          <img
            src={UserIcon}
            alt="User Icon"
            className="user-icon w-14 mx-auto my-5"
          />

          <form
            onSubmit={handleSubmit}
            className="flex flex-col items-center justify-center"
          >
            <div className="flex flex-col items-center justify-center w-full gap-1">
              <input
                type="text"
                placeholder="Username"
                className={`input-field w-[70%] ${validUser ? "border-green-500" : "border-red-500"}`}
                value={user}
                onChange={(e) => setUser(e.target.value)}
              />
              {!validUser && user ? (
                <p className="text-center mx-auto text-red-500 w-4/5 h-14">
                  Invalid: start with "U_" followed by numbers.
                </p>
              ) : (
                <p className="h-14"></p>
              )}
            </div>
            <button className="btn-primary px-3 py-2">Log In</button>
          </form>
        </Card>
        {/* </div> */}
      </div>
    </>
  );
};

export default LogIn;
