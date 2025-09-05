import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend, Title } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend, Title);

const StudentPieChart = () => {
  const data = {
    labels: ["Class 6", "Class 7", "Class 8"], 
    datasets: [
      {
        label: "Registered Students",
        data: [120, 90, 150],
        backgroundColor: ["#5b99f5ff", "#87195fd6", "#ffc107"],
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text:"Registered Students by Class",
        font: {
          size: 20, 
          weight: "bold",
        },
      },
      legend: {
        position: "bottom",
        labels: {
          font: {
            size: 10,
          },
        },
      },
    },
  };

  return (
    <div style={{ height: "350px" }}>
      <Pie data={data} options={options} />
    </div>
  );
};

export default StudentPieChart;
