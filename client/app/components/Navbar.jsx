import React from 'react';

export class Navbar extends React.Component {
   render() {
      return (
         <div className="ui pointing menu">
            <NavbarItem text="Home" />
            <NavbarItem text="Settings" />
         </div>
      );
   }
}

class NavbarItem extends React.Component {
   render() {
      return (
         <a className="item">
            { this.props.text }
         </a>
      );
   }
}
