import { useState } from 'react'
import {
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Button,
  Form,
  FormGroup,
  Label,
  Input
} from 'reactstrap'

const AddNewModal = ({ open, handleModal, onAddTeacher, existingPhones }) => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    registeredClass: '',
    registrationDate: new Date().toISOString().split('T')[0],
    status: 'Active'
  })

  const handleChange = e => {
    const { name, value } = e.target
    setFormData({ ...formData, [name]: value })
  }

  const handleSubmit = e => {
    e.preventDefault()
    if (!/^\d{10}$/.test(formData.phone)) {
      alert('Please enter a valid 10-digit phone number')
      return
    }
    if (existingPhones.includes(formData.phone)) {
      alert('This phone number is already assigned to another teacher')
      return
    }

    onAddTeacher(formData) 

    setFormData({
      name: '',
      email: '',
      phone: '',
      registeredClass: '',
      registrationDate: new Date().toISOString().split('T')[0],
      status: 'Active'
    })
  }

  return (
    <Modal isOpen={open} toggle={handleModal}>
      <ModalHeader toggle={handleModal}>Add New Teacher</ModalHeader>
      <Form onSubmit={handleSubmit}>
        <ModalBody>
          <FormGroup>
            <Label for='name'>Name</Label>
            <Input
              id='name'
              name='name'
              value={formData.name}
              onChange={handleChange}
              required
            />
          </FormGroup>

          <FormGroup>
            <Label for='email'>Email</Label>
            <Input
              type='email'
              id='email'
              name='email'
              value={formData.email}
              onChange={handleChange}
              required
            />
          </FormGroup>

          <FormGroup>
            <Label for='phone'>Phone</Label>
            <Input
              type='text'
              id='phone'
              name='phone'
              value={formData.phone}
              onChange={e => {
                const value = e.target.value
                if (/^\d{0,10}$/.test(value)) handleChange(e)
              }}
              maxLength='10'
              placeholder='Enter 10-digit phone number'
              required
            />
          </FormGroup>

          <FormGroup>
            <Label for='registeredClass'>Registered Class</Label>
            <Input
              type='select'
              id='registeredClass'
              name='registeredClass'
              value={formData.registeredClass}
              onChange={handleChange}
              required
            >
              <option value=''>Select Class</option>
              <option value='Class 6'>Class 6</option>
              <option value='Class 7'>Class 7</option>
              <option value='Class 8'>Class 8</option>
            </Input>
          </FormGroup>
        </ModalBody>
        <ModalFooter>
          <Button color='secondary' onClick={handleModal}>
            Cancel
          </Button>
          <Button color='primary' type='submit'>
            Submit
          </Button>
        </ModalFooter>
      </Form>
    </Modal>
  )
}

export default AddNewModal;