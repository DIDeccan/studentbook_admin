import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchStudentDistribution } from '../../../redux/studentSlice';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, Title } from 'chart.js';
import { Col, Spinner } from 'reactstrap';

ChartJS.register(ArcElement, Tooltip, Legend, Title);

const StudentPieChart = () => {
  const dispatch = useDispatch();
  const { labels, data, pieLoading, pieError } = useSelector(state => state.students);

  useEffect(() => {
    if (labels.length === 0) {
      dispatch(fetchStudentDistribution());
    }
  }, [dispatch, labels.length]);
  
  if (pieLoading)
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


  if (pieError) return <p className="text-danger text-center">Error: {pieError}</p>;

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Registered Students',
        data,
        backgroundColor: ['#5b99f5ff', '#ffc107', '#28a745', '#87195fd6'].slice(0, data.length),
        borderWidth: 1,
      }
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: { display: true, text: 'Registered Students by Class', font: { size: 18 }, color:'gray' },
      legend: { position: 'bottom', labels: { font: { size: 12, weight: 'bold'} } }
    }
  };

  return (
    <div style={{ height: '350px' }}>
      <Pie data={chartData} options={options} />
    </div>
  );
};

export default StudentPieChart;
