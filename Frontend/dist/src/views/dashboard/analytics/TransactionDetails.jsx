import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchLastTransactions } from "../../../redux/studentSlice";
import { Spinner } from 'reactstrap';

const TransactionDetails = () => {
  const dispatch = useDispatch();
  const { transactions, txnLoading, txnError } = useSelector(state => state.students);

  useEffect(() => {
    if (transactions.length === 0) {
      dispatch(fetchLastTransactions());
    }
  }, [dispatch, transactions.length]);

  if (txnLoading)
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


  if (txnError) return <p style={{ color: "red" }}>Error: {txnError}</p>;

  return (
    <div className="table-responsive p-1 mt-2 ">
       <h2
       className="mb-1"
       style={{
       fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
       fontWeight: 600,
       fontSize: "1.50rem",
       letterSpacing: "0.5px",
     }}
  >
  Last Transactions
</h2>
      <table className="table table-bordered text-center table-hover custom-table">
        <thead className="table-light">
          <tr>
            <th>Transaction ID</th>
            <th>User Name</th>
            <th>Email</th>
            <th>Phone</th>
            <th>Class</th>
            <th>Status</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Payment Mode</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((txn, index) => (
            <tr key={index}>
              <td>{txn.transaction_id || "N/A"}</td>
              <td>{txn.user_name}</td>
              <td>{txn.user_email}</td>
              <td>{txn.student_phone}</td>
              <td>{txn.class_name}</td>
                <td>
                {txn.status === "completed" ? (
                    <span className="badge rounded-pill bg-light-success">
                      Completed
                    </span>
                ) : txn.status === "failed" ? (
                    <span className="badge rounded-pill bg-light-danger">
                      Failed
                    </span>
                ) : txn.status === "pending" ? (
                <span className="badge rounded-pill bg-light-warning ">
                      Pending
                   </span>
                ) : (
                  <span className="badge rounded-pill bg-light-secondary">
                {txn.status}
                </span>
                )}
                </td>
              <td>₹{txn.amount}</td>
              <td>{new Date(txn.date).toLocaleString()}</td>
              <td>{txn.payment_mode || "Null"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TransactionDetails;
