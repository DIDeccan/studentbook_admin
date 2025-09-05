import { Fragment, useState, useEffect } from 'react'
import AddNewModal from './addteacherdetails'
import {
  Card,
  CardHeader,
  CardTitle,
  Button,
  Input,
  Label,
  Row,
  Col,
  Table,
  Badge
} from 'reactstrap'

const LOCAL_KEY = 'teachers_list_v1'

const Teachertable = () => {
  const [modal, setModal] = useState(false)
  const [searchValue, setSearchValue] = useState('')
  const [teachers, setTeachers] = useState([])
  const [filteredData, setFilteredData] = useState([])
  const sampleData = [
    {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      phone: '9876543210',
      registeredClass: 'Class 6',
      registrationDate: '2023-01-10',
      status: 'Active'
    },
    {
      id: 2,
      name: 'Jane Smith',
      email: 'jane@example.com',
      phone: '9123456780',
      registeredClass: 'Class 7',
      registrationDate: '2023-02-15',
      status: 'Inactive'
    },
    {
      id: 3,
      name: 'Mike Johnson',
      email: 'mike@example.com',
      phone: '9988776655',
      registeredClass: 'Class 8',
      registrationDate: '2023-03-20',
      status: 'Active'
    }
  ]
  useEffect(() => {
    const stored = localStorage.getItem(LOCAL_KEY)
    if (stored) {
      const parsed = JSON.parse(stored)
      setTeachers(parsed)
      setFilteredData(parsed)
    } else {
      setTeachers(sampleData)
      setFilteredData(sampleData)
      localStorage.setItem(LOCAL_KEY, JSON.stringify(sampleData))
    }
  }, [])

  // Persist on change
  useEffect(() => {
    localStorage.setItem(LOCAL_KEY, JSON.stringify(teachers))
  }, [teachers])

  const handleModal = () => setModal(!modal)

  // Add teacher (from modal)
  const handleAddTeacher = newTeacher => {
    const teacherWithId = { ...newTeacher, id: Date.now() }
    const updated = [...teachers, teacherWithId]
    setTeachers(updated)
    setFilteredData(applyFilter(updated, searchValue))
  }

  // Delete teacher
  const handleDelete = id => {
    const updated = teachers.filter(t => t.id !== id)
    setTeachers(updated)
    setFilteredData(applyFilter(updated, searchValue))
  }

  // Search filter
  const applyFilter = (list, value) => {
    if (!value) return list
    const v = value.toLowerCase()
    return list.filter(item =>
      item.name.toLowerCase().includes(v) ||
      item.email.toLowerCase().includes(v) ||
      item.phone.toLowerCase().includes(v) ||
      item.registeredClass.toLowerCase().includes(v) ||
      item.registrationDate.toLowerCase().includes(v) ||
      item.status.toLowerCase().includes(v)
    )
  }

  const handleFilter = e => {
    const value = e.target.value
    setSearchValue(value)
    setFilteredData(applyFilter(teachers, value))
  }

  return (
    <Fragment>
      <Card>
        <CardHeader className='d-flex justify-content-between align-items-center'>
          <CardTitle tag='h4'>Teacher Details</CardTitle>
          <Button color='primary' onClick={handleModal}>
            + Add Teacher
          </Button>
        </CardHeader>

        <Row className='justify-content-end mx-0 mb-2'>
          <Col md='4' sm='12'>
            <Label for='search-input' className='mb-0'>
              Search
            </Label>
            <Input
              id='search-input'
              type='text'
              value={searchValue}
              onChange={handleFilter}
              placeholder='Search by any field...'
            />
          </Col>
        </Row>
        <div className='table-responsive'>
          <Table striped hover bordered className='mb-0 text-center'>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Class</th>
                <th>Registration Date</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.length ? (
                filteredData.map(item => (
                  <tr key={item.id}>
                    <td>{item.name}</td>
                    <td>{item.email}</td>
                    <td>{item.phone}</td>
                    <td>{item.registeredClass}</td>
                    <td>{item.registrationDate}</td>
                    <td>
                      <Badge
                        color={item.status === 'Active' ? 'success' : 'secondary'}
                      >
                        {item.status}
                      </Badge>
                    </td>
                    <td>
                      <Button
                        size='sm'
                        color='danger'
                        onClick={() => handleDelete(item.id)}
                      >
                        Delete
                      </Button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan='7' className='text-center text-muted'>
                    No records found
                  </td>
                </tr>
              )}
            </tbody>
          </Table>
        </div>
      </Card>

      {/* Modal */}
      <AddNewModal
        open={modal}
        handleModal={handleModal}
        onAddTeacher={handleAddTeacher}
        existingPhones={teachers.map(t => t.phone)} 
      />
    </Fragment>
  )
}

export default Teachertable;