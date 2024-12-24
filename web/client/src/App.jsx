import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import LogIn from "./pages/LogIn";
import Missing from "./pages/Missing";
import Details from "./pages/Details";
import Layout from "./components/Layout";
import "./App.css";

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="/login" element={<LogIn />} />
        <Route path="/details/:id_course" element={<Details />} />
        <Route path="/home" element={<Home />} />
        <Route path="/" element={<LogIn />} />
      </Route>
      <Route path="/*" element={<Missing />} />
    </Routes>
  );
};
export default App;
