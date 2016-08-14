import React from 'react';

import { Navbar } from './Navbar.jsx';
import { Sidebar } from './Sidebar.jsx';

export class Navigation extends React.Component {
  render() {
    return (
      <nav className="navbar navbar-default navbar-static-top" role="navigation" style={{marginBottom: "0"}}>
        <Navbar />
        <Sidebar />
      </nav>
    );
  }
}
