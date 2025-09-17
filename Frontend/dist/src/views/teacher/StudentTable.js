import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchUserDetails } from "../../redux/userSlice";
import { Spinner } from "reactstrap";


const StudentTable = () => {
  const dispatch = useDispatch();
  const { users, userLoading, userError } = useSelector((state) => state.user);

  const [search, setSearch] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const usersPerPage = 10; 

  useEffect(() => {
    if (users.length === 0) {
      dispatch(fetchUserDetails());
    }
  }, [dispatch, users.length]);

  const filteredUsers = users.filter(
    (user) =>
      user.name?.toLowerCase().includes(search.toLowerCase()) ||
      user.email?.toLowerCase().includes(search.toLowerCase()) ||
      user.phone?.toLowerCase().includes(search.toLowerCase()) ||
      user.status?.toLowerCase().includes(search.toLowerCase()) ||
      user.subscription_plan?.toLowerCase().includes(search.toLowerCase())
  );

  // Pagination logic
  const totalPages = Math.ceil(filteredUsers.length / usersPerPage);
  // startIndex = (2 - 1) * 10 = 10,
  const startIndex = (currentPage - 1) * usersPerPage;
  // if startindex 0 and usersperpage is 10 then slice(0,10)=0-9
  const currentUsers = filteredUsers.slice(startIndex, startIndex + usersPerPage);

 if (userLoading)
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

  if (userError)
    return <p className="text-danger text-center">Error: {userError}</p>;

  return (
    <div className="table-responsive p-1 mt-1">
      <div className="d-flex justify-content-between align-items-center mb-2">
        <h5 className="mb-1 fs-4 fw-bold fs-4 mt-1">User Login Details</h5>
        <input
          type="text"
          placeholder="Search by name, email, phone, status..."
          className="form-control w-25"
          value={search}
          onChange={(e) => {
            setSearch(e.target.value);
            setCurrentPage(1); 
          }}
        />
      </div>
      <table className="table table-bordered text-center table-hover custom-table mb-0">
        <thead className="table-light">
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Registered Class</th>
            <th>Registered Date</th>
            <th>Last Login</th>
            <th>Status</th>
            <th>Subscription Plan</th>
          </tr>
        </thead>
        <tbody>
          {currentUsers.length > 0 ? ( 
            currentUsers.map((user, index) => (
              <tr key={index}>
                <td>{user.name || "N/A"}</td>
                <td>{user.email || "N/A"}</td>
                <td>{user.phone || "N/A"}</td>
                <td>{user.registered_class || "N/A"}</td>
                <td>{user.registered_date || "N/A"}</td>
                <td>{user.last_login_time || "N/A"}</td>
                <td>
                  {user.status === "Active" ? (
                    <span className="badge rounded-pill bg-light-success">
                      Active
                    </span>
                  ) : (
                    <span className="badge rounded-pill bg-light-danger">
                      Inactive
                    </span>
                  )}
                </td>
                <td>{user.subscription_plan || "No Subscription"}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="8">No users found</td>
            </tr>
          )}
        </tbody>
      </table>

      {totalPages > 1 && (
        <div className="d-flex justify-content-between align-items-center mt-2 mb-0 px-1 ">
          <small className="text-muted">
            Showing {startIndex + 1} -{" "}
            {Math.min(startIndex + usersPerPage, filteredUsers.length)} of{" "}
            {filteredUsers.length} users
          </small>
          
          <nav>
            <ul className="pagination mb-2">
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

export default StudentTable;
