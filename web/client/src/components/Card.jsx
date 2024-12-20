import React, { useEffect } from "react";

import "./Card.css";

const Card = ({ children, className, key, radius, color }) => {
  useEffect(() => {
    const handleMouseMove = (e) => {
      const cards = document.getElementsByClassName("card");
      for (const card of cards) {
        const rect = card.getBoundingClientRect(),
          x = e.clientX - rect.left,
          y = e.clientY - rect.top;

        card.style.setProperty("--mouse-x", `${x}px`);
        card.style.setProperty("--mouse-y", `${y}px`);
      }
    };

    const cardsContainer = document.getElementsByClassName("cards");
    // console.log(cardsContainer);
    if (!cardsContainer) return;
    Array.from(cardsContainer).forEach((card) => {
      card.addEventListener("mousemove", handleMouseMove);
    });

    return () => {
      Array.from(cardsContainer).forEach((card) => {
        card.removeEventListener("mousemove", handleMouseMove);
      });
    };
  }, []);

  return (
    <div
      className={`card ${className}`}
      key={key || ""}
      style={{ "--radius": radius, "backgroundColor": color }}
    >
      <div className={`card-content ${className}`}>{children}</div>
    </div>
  );
};

export default Card;
