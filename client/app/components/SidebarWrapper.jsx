import React from 'react';

import { Sidebar } from './Sidebar.jsx';
import { Grid } from './Grid.jsx';
import { Navbar } from './Navbar.jsx';

var navbarItems = [
   {text: "Home", url: "/"},
   {text: "Notifications", url: "/"},
   {text: "Log", url: "/"}
];

var dropdownNavbarItems = [
   {text: "Settings", url: "/"},
   {text: "Logout", url: "/"}
];

export class SidebarWrapper extends React.Component {
   render() {
      return (
         <div>
            <div className="ui large left vertical visible menu inverted sidebar">
               <SidebarTitle />
               <ScriptListMenu />
            </div>
            <Navbar
               items={navbarItems}
               dropdownItems={dropdownNavbarItems}
            />
            <div className="pusher">
               <Grid />
            </div>
         </div>
      );
   }
}

class SidebarTitle extends React.Component {
   render() {
      return (
         <div className="item">
            <a href="/">
               <h2>Dash</h2>
            </a>
         </div>
      );
   }
}

class ScriptListMenu extends React.Component {
   render () {
      return (
         <div className="item">
            <h3>Scripts</h3>
            <div className="menu">
               <a className="active item" href="/introduction/integrations.html">
                  Integrations
                  <div className="ui teal left pointing label">1</div>
               </a>
               <a className="item" href="/introduction/integrations.html">
                  Build Tools
               </a>
            </div>
         </div>
      );
   }
}