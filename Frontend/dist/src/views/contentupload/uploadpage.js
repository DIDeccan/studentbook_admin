import React, { useState, useEffect } from "react";
import {
  Form,
  FormGroup,
  Label,
  Input,
  Button,
  Card,
  CardBody,
  CardTitle,
  Row,
  Col,
} from "reactstrap";
import axios from "axios";

const UploadLearningVideo = () => {
  const [formData, setFormData] = useState({
    class: "",
    subject: "",
    semester: "",
    chapter_number: "",
    chapter_name: "",
    subchapter: "",
    videoName: "",
    videoFile: null,
  });

  const [classData, setClassData] = useState([]);
  const [subjects, setSubjects] = useState([]);

  // ✅ Fetch classes with subjects
  useEffect(() => {
    axios
      .get("http://127.0.0.1:8001/classes_with_subjects/")
      .then((res) => {
        setClassData(res.data.data);
      })
      .catch((err) => {
        console.error("Error fetching data:", err);
      });
  }, []);

 const handleChange = (e) => {
  const { name, value } = e.target;

  setFormData({
    ...formData,
    [name]: name === "chapter_number" ? Number(value) : value,
  });

  if (name === "class") {
    const selectedClass = classData.find(
      (cls) => cls.class_id === parseInt(value)
    );
    setSubjects(selectedClass ? selectedClass.subjects : []);
    setFormData((prev) => ({ ...prev, subject: "" }));
  }
};


  const handleFileChange = (e) => {
    setFormData({ ...formData, videoFile: e.target.files[0] });
  };

const handleSubmit = async (e) => {
  e.preventDefault();

  // ✅ Build form data for file upload
  const payload = new FormData();
  payload.append("class_id", formData.class);
  payload.append("subject_id", formData.subject);
  payload.append("semester", formData.semester);
  payload.append("chapter_number", formData.chapter_number);
  payload.append("chapter_name", formData.chapter_name);
  payload.append("subchapter", formData.subchapter);
  payload.append("video_name", formData.videoName);
  payload.append("video_file", formData.videoFile);

  // ✅ Debug: print formdata in console
  for (let [key, value] of payload.entries()) {
    console.log(key, value);
  }

  try {
    const res = await axios.post(
      "http://127.0.0.1:8001/video_upload",
      payload,
      {
        headers: { "Content-Type": "multipart/form-data" },
      }
    );
    console.log("Upload Success:", res.data);
    alert("Video uploaded successfully!");
  } catch (err) {
    console.error("Upload Error:", err.response?.data || err.message);
    alert("Failed to upload video!");
  }
};


  const handleReset = () => {
    setFormData({
      class: "",
      subject: "",
      semester: "",
      chapter_number: "",
      chapter_name: "",
      subchapter: "",
      videoName: "",
      videoFile: null,
    });
    setSubjects([]);
  };

  return (
    <div>
      <Card>
        <CardBody>
          <CardTitle tag="h4" className="mb-4 fw-bold text-primary">
            📚 Upload Learning Video
          </CardTitle>

          <Form onSubmit={handleSubmit}>
            {/* Class & Subject */}
            <Row>
              <Col md={6}>
                <FormGroup>
                  <Label for="class">Class</Label>
                  <Input
                    type="select"
                    name="class"
                    id="class"
                    value={formData.class}
                    onChange={handleChange}
                  >
                    <option value="">Select Class</option>
                    {classData.map((cls) => (
                      <option key={cls.class_id} value={cls.class_id}>
                        {cls.class_name}
                      </option>
                    ))}
                  </Input>
                </FormGroup>
              </Col>

              <Col md={6}>
                <FormGroup>
                  <Label for="subject">Subject</Label>
                  <Input
                    type="select"
                    name="subject"
                    id="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    disabled={!formData.class}
                  >
                    <option value="">Select Subject</option>
                    {subjects.map((subj) => (
                      <option key={subj.subject_id} value={subj.subject_id}>
                        {subj.subject_name}
                      </option>
                    ))}
                  </Input>
                </FormGroup>
              </Col>
            </Row>

            {/* Semester */}
            <FormGroup>
              <Label for="semester">Semester</Label>
              <Input
                type="select"
                name="semester"
                id="semester"
                value={formData.semester}
                onChange={handleChange}
              >
                <option value="">Select</option>
                <option value="1">1</option>
                <option value="2">2</option>
              </Input>
            </FormGroup>

            {/* Chapter Number */}
            <FormGroup>
              <Label for="chapter_number">Chapter Number</Label>
              <Input
                type="number"
                name="chapter_number"
                id="chapter_number"
                placeholder="Enter chapter number"
                value={formData.chapter_number}
                onChange={handleChange}
              />
            </FormGroup>

            {/* Chapter Name */}
            <FormGroup>
              <Label for="chapter_name">Chapter Name</Label>
              <Input
                type="text"
                name="chapter_name"
                id="chapter_name"
                placeholder="Enter chapter name"
                value={formData.chapter_name}
                onChange={handleChange}
              />
            </FormGroup>

            {/* Subchapter */}
            <FormGroup>
              <Label for="subchapter">Subchapter</Label>
              <Input
                type="text"
                name="subchapter"
                id="subchapter"
                placeholder="Enter subchapter (e.g., 1.2)"
                value={formData.subchapter}
                onChange={handleChange}
              />
            </FormGroup>

            {/* Video Name */}
            <FormGroup>
              <Label for="videoName">Video Name</Label>
              <Input
                type="text"
                name="videoName"
                id="videoName"
                placeholder="Enter video name"
                value={formData.videoName}
                onChange={handleChange}
              />
            </FormGroup>

            {/* File Upload */}
            <FormGroup>
              <Label for="videoFile">Video File</Label>
              <Input
                type="file"
                id="videoFile"
                accept="video/mp4"
                onChange={handleFileChange}
              />
            </FormGroup>

            {/* Preview */}
            {formData.videoName && formData.videoFile && (
              <div className="border rounded p-3 mb-3">
                <p className="mb-1 text-primary">
                  Class ID: {formData.class} | Subject ID: {formData.subject} | Semester{" "}
                  {formData.semester}
                </p>
                <p className="mb-1">
                  Chapter {formData.chapter_number} - {formData.chapter_name} | Subchapter{" "}
                  {formData.subchapter}
                </p>
                <p className="fw-bold text-info">{formData.videoName}</p>
                <p className="text-success mb-0">
                  {formData.videoFile.name} ✅
                </p>
              </div>
            )}

            {/* Buttons */}
            <div className="d-flex justify-content-between">
              <Button color="primary" type="submit">
                Upload Video
              </Button>
              <Button color="secondary" type="button" onClick={handleReset}>
                Reset Form
              </Button>
            </div>
          </Form>
        </CardBody>
      </Card>
    </div>
  );
};

export default UploadLearningVideo;
