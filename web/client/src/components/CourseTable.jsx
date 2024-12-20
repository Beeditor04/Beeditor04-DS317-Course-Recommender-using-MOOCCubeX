import React from 'react';
import CourseRow from './CourseRow';
import './CourseTable.css';

const CourseTable = ({courses_data}) => {
    const handleAdd = (id) => {
        console.log(`Add course with id: ${id}`);
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
          {courses_data.map((course, index) => (
            <CourseRow 
              key={course.id} 
              course={course} 
              onAdd={handleAdd} 
              onDelete={handleDelete} 
              type={index % 2}
            />
          ))}
        </tbody>
    </table> 
        </>
    )
}

export default CourseTable;