import React from 'react';
import CourseRow from './CourseRow';
import './CourseTable.css';
import axios from '../api/axios';
import { useState } from 'react';

const CourseTable = ({courses_data, length, user_course, user_id}) => {
    console.log("CourseTable: ", courses_data, length, user_course); 

    const handleAdd = async (id) => {
        console.log(`Add course with id: ${id}`);
          try {
            const response = await axios.post("/add/" + user_id + "/" + id);
            console.log(`Course ${id} added for user ${user_id}`);
          } catch (err) {
            console.error("Error adding course:", err);
          }
        // Add logic
      };
    
      const handleDelete = (id) => {
        console.log(`Delete course with id: ${id}`);
        // Delete logic
      };
    return (
        <>
                <table className="courses-table">
        <thead>
          <tr>
            <th className="text-purple-300">Id</th>
            <th className="text-purple-300">Name</th>
            <th className="text-purple-300">Prerequisites</th>
            <th className="text-purple-300">Action</th>
          </tr>
        </thead>
        <tbody>
          {courses_data
          .slice(0, length)
          .map((course, index) => (
            <CourseRow 
              key={course.id} 
              course={course} 
              onAdd={handleAdd} 
              onDelete={handleDelete} 
              type={index % 2}
              isRegistered={user_course.includes(course.id)}
            />
          ))}
        </tbody>        
    </table> 

        </>
    )
}

export default CourseTable;