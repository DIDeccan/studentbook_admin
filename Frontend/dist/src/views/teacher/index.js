import { Col } from 'reactstrap'
import StudentTable from './StudentTable';



const TeacherDetails = () => {
    return (
        <Col md="12">
          <div className="card shadow-md w-100 h-80">
            <div className="card-body p-0">
              <StudentTable/>
            </div>
          </div>
        </Col>
    )
}

export default TeacherDetails;

