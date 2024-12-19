import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

const Details = () => {
  const { id } = useParams();
  return (
    <div className="container mx-auto">
      <h1 className="text-4xl text-center m-10">Hello Details {id}</h1>
    </div>
  );
};

export default Details;
