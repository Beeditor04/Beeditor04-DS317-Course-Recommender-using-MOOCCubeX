import { Link } from "react-router-dom";

const Missing = () => {
  return (
    <div className="wrapper flex flex-col items-center justify-center h-screen gap-5">
      <h1>Missing</h1>
      <p>You are lost into the Shadow Realm.</p>
      <Link class="btn-primary px-3 py-2" to="/home" >
        Back to Home
      </Link>
    </div>
  );
};

export default Missing;
