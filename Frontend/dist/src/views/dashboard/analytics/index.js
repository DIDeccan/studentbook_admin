import { Container, Row, Col } from "reactstrap";
import StudentPieChart from "./StudentPiechart";
import TransactionDetails from "./TransactionDetails";
import SampleUserTable from "./LoginDetails";

const Dashboard = () => {
  return (
    <Container fluid>
      <style>
             {`
          .table td, .table th {
            padding-left: 1rem !important;
            vertical-align: middle !important;
          }
          .table td:first-child {
            padding-left: 1.5rem !important; /* more space for CARD column */
          }
        `}
      </style>
    
      <Row className="mb-3">
        <Col>
          <h4>Dashboard</h4>
        </Col>
      </Row>
      <Row className="align-items-stretch">
        <Col md="6" className="d-flex">
          <div className="card shadow-sm w-100 h-100">
            <div className="card-body d-flex justify-content-center align-items-center">
              <StudentPieChart />
            </div>
          </div>
        </Col>
        <Col md="6" className="d-flex ">
          <div className="card shadow-sm w-100 h-100">
            <div className="card-header fw-bold">Last Transaction</div>
            <div className="card-body p-0 ">
              <TransactionDetails />
            </div>
          </div>
        </Col>
        </Row>
        <Row>
         <Col md="12" className="d-flex mt-5">
          <div className="card shadow-sm w-100 h-100">
            <div className="card-header fw-bold">User Login Details</div>
            <div className="card-body p-0">
              <SampleUserTable/>
            </div>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;
