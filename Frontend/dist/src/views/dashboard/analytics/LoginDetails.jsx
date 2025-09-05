import React from 'react';

const SampleUserTable = () =>{
    const users = [
    {
        name: "John Doe",
        email:"john@example.com",
        loginTime:"09:00 AM",
        logoutTime:"05:00 PM",
        ip:"192.168.1.10",
        status:"Active",
    },
    {
        name:"Jane Smith",
        email:"Jane@example.com",
        loginTime: "09:30 AM",
        logoutTime: "05:30 PM",
        ip: "192.168.1.11",
        status: "Inactive",
    },
    {
      name: "Johnson",
      email: "Johnson@example.com",
      loginTime: "08:45 AM",
      logoutTime: "04:45 PM",
      ip: "192.168.1.12",
      status: "Active",
    },
    {
        name:"Smith",
        email:"Smith@example.com",
        loginTime: "09:00 AM",
        logoutTime: "05:00 PM",
        ip: "192.168.1.13",
        status: "Inactive",
    },
    {
      name: "Bob",
      email: "bob@example.com",
      loginTime: "08:30 AM",
      logoutTime: "04:30 PM",
      ip: "192.168.1.14",
      status: "Active",
    },
    ];
    return(
        <div className="table-responsive">
          <table className='table table bordered table-striped'>
            <thead className='table-light'>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Login Time</th>
                <th>Logout Time</th>
                <th>IP</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
                {users.map((user, index) => (
                    <tr key={index}>
                       <td>{user.name}</td>
                       <td>{user.email}</td>
                       <td>{user.loginTime}</td>
                       <td>{user.logoutTime}</td>
                       <td>{user.ip}</td>
                       <td className={user.status === "Active" ? "text-success" : "text-danger"}>
                        {user.status}
                       </td>
                    </tr>
                ))}
            </tbody>
        </table>
        </div>
    );
};

export default SampleUserTable;