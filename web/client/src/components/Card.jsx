import React, { useEffect } from "react";

import "./Card.css";

const Card = ({ children, className, ...props }) => {
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
    
        const cardsContainer = document.getElementsByClassName("cards")[0];
        if (cardsContainer) {
          cardsContainer.addEventListener("mousemove", handleMouseMove);
        }
    
        return () => {
          if (cardsContainer) {
            cardsContainer.removeEventListener("mousemove", handleMouseMove);
          }
        };
      }, []);
  return (
        <div className={`card ${className}`} {...props}>
            <div className="card-content">
                {children}
            </div>
        </div>

  );
};


export default Card;
