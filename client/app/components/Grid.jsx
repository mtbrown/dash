import React from 'react';

import { Navbar } from './Navbar.jsx';
import { Sidebar } from './Sidebar.jsx';

var navbarItems = [
   {text: "Home", url: "/"},
   {text: "Notifications", url: "/"},
   {text: "Log", url: "/"}
];

var dropdownNavbarItems = [
   {text: "Settings", url: "/"},
   {text: "Logout", url: "/"}
];

export class Grid extends React.Component {
   render() {
      return (
         <div className="ui grid">
               <div className="four wide column">
                  
               </div>
            
         </div>
      );
   }
}