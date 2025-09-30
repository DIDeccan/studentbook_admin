import { Container, Row, Col } from "reactstrap";
import TransactionDetails from "./TransactionDetails";
import StudentPieChart from "./StudentPiechart";
import LoginDetails from "./LoginDetails";
// import '../../../@core/scss/base/pages/app-student.scss';


const Dashboard = () => {
  return (
    <Container fluid>
      <Row>
        <Col md="6" className="mb-2 mt-2">
          <div className="card shadow-md w-100 h-80">
            <div className="card-body d-flex justify-content-center align-items-center">
              <StudentPieChart />
            </div>
          </div>
        </Col>

        <Col md="12" className="mb-2">
          <div className="card shadow-md w-100 h-80">
            <div className="card-body p-0">
              <TransactionDetails />
            </div>
          </div>
        </Col>

        <Col md="12" className="mb-2">
          <div className="card shadow-md w-100 h-80">
            <div className="card-body p-0">
              <LoginDetails />
            </div>
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;
