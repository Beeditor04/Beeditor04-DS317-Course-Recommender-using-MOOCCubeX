import React from 'react';
import { Link } from 'react-router-dom';
const LIMIT_LENGTH = 50;

const truncateString = (str) => {
  if (!str) return "";
  return str.length > LIMIT_LENGTH ? str.slice(0, LIMIT_LENGTH) + "..." : str;
};

const CourseRow = ({ course, onAdd, onDelete, type, isRegistered }) => {
  return (
    <tr
      className="text-center"
      style={{ backgroundColor: type === 0 ? 'var(--neutral-800)' : 'var(--neutral-700)' }}
    >
      <td style={{ color: "var(--neutral-200)" }}>
        <Link to={`/details/${course.id}`} state={{ course: course }}>
          {truncateString(course.id)}
        </Link>
      </td>
      <td>
        <Link to={`/details/${course.id}`} state={{ course: course }}>
          {truncateString(course.name)}
        </Link>
      </td>
      <td style={{ color: "var(--neutral-200)" }}>
        <Link to={`/details/${course.id}`} state={{ course: course }}>
          {truncateString(course.prerequisites)}
        </Link>
      </td>
      <td>
        {!isRegistered ? (
          <button className="status-yes mr-1 mb-1" onClick={() => onAdd(course.id)}>Add</button>
        ) : (
          <button className="status-no" onClick={() => onDelete(course.id)}>Delete</button>
        )}
      </td>
    </tr>
  );
};

export default CourseRow;