import React, { useState } from "react";
import Select from "react-select";
import { useDispatch, useSelector } from "react-redux";
import { fetchPaymentDetails } from "../../redux/paymentSlice";
import { Spinner } from "reactstrap";
import { FileText } from "react-feather";

const classOptions = [
  { value: "Class 6", label: "Class 6" },
  { value: "Class 7", label: "Class 7" },
  { value: "Class 8", label: "Class 8" },
  { value: "Class 9", label: "Class 9" },
  { value: "Class 10", label: "Class 10" },
];

const statusOptions = [
  { value: "completed", label: "Completed" },
  { value: "failed", label: "Failed" },
  { value: "pending", label: "Pending" },
];

const PaymentDetails = () => {
  const dispatch = useDispatch();
  const { payments, loading, error } = useSelector((state) => state.payments);

  const [filters, setFilters] = useState({
    start_date: "",
    end_date: "",
    class: null,
    status: null,
  });

  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value,
    });
  };

  const handleSelectChange = (selectedOption, actionMeta) => {
    setFilters({
      ...filters,
      [actionMeta.name]: selectedOption,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);

    const apiFilters = {
      start_date: filters.start_date || "",
      end_date: filters.end_date || "",
      class: filters.class ? filters.class.value : "",
      status: filters.status ? filters.status.value : "",
    };

    dispatch(fetchPaymentDetails(apiFilters));
  };

  // ✅ Converts array to CSV format
  function convertArrayOfObjectsToCSV(array) {
    if (!array || array.length === 0) return null;
   
    //columns are separated by commas.
    const columnDelimiter = ",";
    //rows are separated by newlines.
    const lineDelimiter = "\n";
    //These will be the column names and the order
    const keys = Object.keys(array[0]);
    //id,name,age\n
    let result = keys.join(columnDelimiter) + lineDelimiter;

    array.forEach((item) => {
      let line = "";
      keys.forEach((key, index) => {
        if (index > 0) line += columnDelimiter;
        line += item[key] !== null && item[key] !== undefined ? item[key] : "";
      });
      result += line + lineDelimiter;
    });

    return result;
  }

  // ✅ Triggers CSV download
  function downloadCSV(array) {
    const csv = convertArrayOfObjectsToCSV(array);
    if (csv === null) return;

    const filename = "payment_details.csv";
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });

    const link = document.createElement("a");
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob);
      link.setAttribute("href", url);
      link.setAttribute("download", filename);
      link.style.visibility = "hidden";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }

  return (
      <div className="container-fluid p-0">
  <div className="card shadow-sm w-100 mb-3">
    <div className="card-header pt-4 pb-0 ps-2 pe-3">
      <h4 className="fw-bold fs-4 mb-3">Payment Details</h4> </div>
        <div className="card-body pt-2 pb-2 ps-3 pe-3 ">
          <form onSubmit={handleSubmit}>
            <div className="row g-3 mb-4">
              <div className="col-md-6">
                <label className="form-label fw-semibold">Start Date</label>
                <input
                  type="date"
                  name="start_date"
                  value={filters.start_date}
                  onChange={handleChange}
                  className="form-control"
                  max={filters.end_date || undefined}
                />
              </div>
              <div className="col-md-6">
                <label className="form-label fw-semibold">End Date</label>
                <input
                  type="date"
                  name="end_date"
                  value={filters.end_date}
                  onChange={handleChange}
                  className="form-control"
                  min={filters.start_date || undefined}
                />
              </div>
            </div>

            <div className="row g-3 mb-4">
              <div className="col-md-6">
                <label className="form-label fw-semibold">Class</label>
                <Select
                  options={classOptions}
                  name="class"
                  value={filters.class}
                  onChange={handleSelectChange}
                  placeholder="Select Class"
                  isClearable
                  classNamePrefix="select" 
                />
              </div>
              <div className="col-md-6">
                <label className="form-label fw-semibold">Status</label>
                <Select
                  options={statusOptions}
                  name="status"
                  value={filters.status}
                  onChange={handleSelectChange}
                  placeholder="Select Status"
                  isClearable
                  classNamePrefix="select" 
                />
              </div>
            </div>

            <div className="row mt-4 mb-1">
              <div className="col text-end">
                <button type="submit" className="btn btn-primary px-4">
                  Submit
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>

      {submitted && loading && (
        <div
          className="d-flex justify-content-center align-items-center border rounded shadow-sm loader-box"
          style={{ height: "200px" }}
        >
          <Spinner color="primary" style={{ width: "3rem", height: "3rem" }} />
        </div>
      )}

      {submitted && error && (
        <p className="text-danger text-center mt-3">Error: {error}</p>
      )}

      {submitted && !loading && !error && (
        <div className="card shadow-md mt-2 mb-2">
          <div className="d-flex justify-content-end p-2 gap-2">
            <button
              onClick={() => downloadCSV(payments)}
              className="btn btn-outline-success btn-md d-flex align-items-center m-2 mt-0 mb-0"
            >
              <FileText size={15} className="me-50" />
              <span className="align-middle">Export CSV</span>
            </button>
          </div>
          <div className="card-body pt-0 pb-2 ps-3 pe-3">
            <div className="table-responsive">
              <table className="table table-bordered align-middle text-center table-hover custom-table">
                <thead className="table-light">
                  <tr>
                    <th>Transaction ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Class</th>
                    <th>Status</th>
                    <th>Payment Mode</th>
                    <th>Gateway</th>
                    <th>Start Date</th>
                    <th>End Date</th>
                  </tr>
                </thead>
                <tbody>
                  {payments.length > 0 ? (
                    payments.map((p) => (
                      <tr key={p.transaction_id || Math.random()}>
                        <td>{p.transaction_id || "N/A"}</td>
                        <td>{p.user_name}</td>
                        <td>{p.user_email}</td>
                        <td>{p.class}</td>
                        <td>
                          {p.status === "completed" ? (
                            <span className="badge rounded-pill bg-light-success">
                              Completed
                            </span>
                          ) : p.status === "failed" ? (
                            <span className="badge rounded-pill bg-light-danger">
                              Failed
                            </span>
                          ) : p.status === "pending" ? (
                            <span className="badge rounded-pill bg-light-warning ">
                              Pending
                            </span>
                          ) : (
                            <span className="badge rounded-pill bg-light-secondary">
                              {p.status}
                            </span>
                          )}
                        </td>
                        

                        <td>{p.payment_mode || "N/A"}</td>
                        <td>{p.payment_gateway || "Not Available"}</td>
                        <td>{p.start_date}</td>
                        <td>{p.end_date}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="9" className="text-center">
                        No payments found
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PaymentDetails;
