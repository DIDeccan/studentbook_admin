import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";

const TransactionDetails = () => {
  const transactions = [
    { 
      id: 1,
      cardType: "visa",
      cardNumber: "4230", 
      date: "17 Mar 2022", 
      status: "Verified", 
      amount: "+$1,678" 
    },
    { 
      id: 2, 
      cardType: "mastercard", 
      cardNumber: "5578", 
      date: "12 Feb 2022", 
      status: "Rejected", 
      amount: "-$839" 
    },
    { 
      id: 3, 
      cardType: "amex", 
      cardNumber: "4567", 
      date: "28 Feb 2022", 
      status: "Verified", 
      amount: "+$435" 
    },
    { 
      id: 4, 
      cardType: "visa", 
      cardNumber: "5699", 
      date: "8 Jan 2022", 
      status: "Pending", 
      amount: "+$2,345" 
    },
    { 
      id: 5, 
      cardType: "visa", 
      cardNumber: "5699", 
      date: "8 Jan 2022", 
      status: "Rejected", 
      amount: "-$234" 
    },
  ];

  const getStatusBadge = (status) => {
    switch (status) {
      case "Verified":
        return <span className="badge bg-success">{status}</span>;
      case "Rejected":
        return <span className="badge bg-danger">{status}</span>;
      case "Pending":
        return <span className="badge bg-secondary">{status}</span>;
      default:
        return <span className="badge bg-light text-dark">{status}</span>;
    }
  };

  return (
    <table className="table mb-0 align-middle">
      <thead className="table-light">
        <tr>
          <th>CARD</th>
          <th>DATE</th>
          <th>STATUS</th>
          <th>TREND</th>
        </tr>
      </thead>
      <tbody>
        {transactions.map((tx) => (
          <tr key={tx.id}>
            <td className="align-middle">
              <div className="d-flex align-items-center">
                <span className="ms-2 me-2">💳</span>*{tx.cardNumber}
              </div>
              <small className="text-muted">Credit</small>
            </td>
            <td className="align-middle">
              <div>Sent</div>
              <small className="text-muted">{tx.date}</small>
            </td>
            <td className="align-middle">
              {getStatusBadge(tx.status)}
            </td>
            <td className={tx.amount.startsWith("-") ? "text-danger" : "text-success"}>
              {tx.amount}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default TransactionDetails;
