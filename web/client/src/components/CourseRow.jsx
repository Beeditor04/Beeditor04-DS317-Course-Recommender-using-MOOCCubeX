import React from 'react';
import { Link } from 'react-router-dom';
const CourseRow = ({ course, onAdd, onDelete, type }) => {
  return (
    <tr className="text-center"style={{ backgroundColor: type === 0 ? 'var(--neutral-800)' : 'var(--neutral-700)' }}> 
      <td style={{color: "var(--neutral-200)"}}><Link to={`/details/${course}`} state={{ course: course }}>{course}</Link></td>
      {/* <td style={{color: "var(--neutral-200)"}}><Link to={`/details/${course.id}`} state={{ course: course }}>{course.id}</Link></td> */}
      {/* <td><Link to={`/details/${course.id}`} state={{ course: course }}>{course.name}</Link></td>
      <td style={{color: "var(--neutral-200)"}}><Link to={`/details/${course.id}`} state={{ course: course }}>{course.prerequisites}</Link></td> */}
      <td>
        <button className="status-yes mr-1 mb-1" onClick={() => onAdd(course.id)}>Add</button>
        <button className="status-no" onClick={() => onDelete(course.id)}>Delete</button>
      </td>

    </tr>
  );
};

export default CourseRow;