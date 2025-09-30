import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchUserLoginDetails } from "../../../redux/studentSlice";
import { Spinner } from "reactstrap";

const LoginDetails = () => {
  const dispatch = useDispatch();
  const { userLogins, userLoginLoading, userLoginError, fetched } = useSelector(
    (state) => state.students
  );

  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const usersPerPage = 10; // 🔹 10 per page

  useEffect(() => {
    if (!fetched) {
      dispatch(fetchUserLoginDetails());
    }
  }, [dispatch, fetched]);

  // 🔹 Filtered data
  const filteredUsers = userLogins.filter((user) => {
    const term = searchTerm.toLowerCase();
    return (
      user.name?.toLowerCase().includes(term) ||
      user.email?.toLowerCase().includes(term) ||
      user.status?.toLowerCase().includes(term)
    );
  });

  // 🔹 Pagination
  const totalPages = Math.ceil(filteredUsers.length / usersPerPage);
  const startIndex = (currentPage - 1) * usersPerPage;
  const currentUsers = filteredUsers.slice(startIndex, startIndex + usersPerPage);

  if (userLoginLoading)
    return (
      <div
        style={{
          minHeight: "300px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
        className="w-100"
      >
        <Spinner color="primary" style={{ width: "3rem", height: "3rem" }} />
      </div>
    );

  // 🔹 Error
  if (userLoginError) {
    return <p className="text-danger text-center">Error: {userLoginError}</p>;
  }

  return (
    <div className="table-responsive p-1 mt-1">
      <div className="d-flex justify-content-between align-items-center mb-2">
        <h2
          className="mb-0"
          style={{
            fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
            fontWeight: 600,
            fontSize: "1.50rem",
            letterSpacing: "0.5px",
          }}
        >
          User Details
        </h2>
        <div className="searchable-table-container">
          <input
            type="text"
            placeholder="Search by name, email, status..."
            className="form-control search-input"
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setCurrentPage(1);
            }}
          />
        </div>
      </div>

      {/* Table */}
      <table className="table table-bordered text-center table-hover custom-table">
        <thead className="table-light">
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Last Login</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {currentUsers.length > 0 ? (
            currentUsers.map((user, index) => (
              <tr key={index}>
                <td>{user.name || "N/A"}</td>
                <td>{user.email || "N/A"}</td>
                <td>
                  {user.login_time
                    ? new Date(user.login_time).toLocaleString()
                    : "N/A"}
                </td>
                <td>
                  {user.status === "Active" ? (
                    <span className="badge rounded-pill bg-light-success">Active</span>
                  ) : (
                    <span className="badge rounded-pill bg-light-danger">Inactive</span>
                  )}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="4">No users found</td>
            </tr>
          )}
        </tbody>
      </table>

      {totalPages > 1 && (
        <div className="d-flex justify-content-between align-items-center mt-1">
          <small className="text-muted">
            Showing {startIndex + 1} -{" "}
            {Math.min(startIndex + usersPerPage, filteredUsers.length)} of{" "}
            {filteredUsers.length} users
          </small>

          <nav>
            <ul className="pagination mb-0">
              <li className={`page-item ${currentPage === 1 ? "disabled" : ""}`}>
                <button
                  className="page-link"
                  onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                >
                  Previous
                </button>
              </li>
              <li className="page-item disabled">
                <span className="page-link">
                  Page {currentPage} of {totalPages}
                </span>
              </li>
              <li
                className={`page-item ${
                  currentPage === totalPages ? "disabled" : ""
                }`}
              >
                <button
                  className="page-link"
                  onClick={() =>
                    setCurrentPage((prev) => Math.min(prev + 1, totalPages))
                  }
                >
                  Next
                </button>
              </li>
            </ul>
          </nav>
        </div>
      )}
    </div>
  );
};

export default LoginDetails;