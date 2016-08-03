import React from 'react';

export class Navbar extends React.Component {
   render() {
      var navbarItemNodes = this.props.items.map(function(item, i) {
         return <NavbarItem text={item.text} key={i} />;
      });

      return (
         <div className="ui top fixed inverted menu">
            <div className="header large item">{ this.props.title }</div>
            { navbarItemNodes }
            <div className="right menu">
               <DropdownMenu items={this.props.dropdownItems} />
            </div>
         </div>
      );
   }
}

class DropdownMenu extends React.Component {
   render () {
      var dropdownItemNodes = this.props.items.map(function(item, i) {
         return <NavbarItem text={item.text} key={i} />;
      });

      return (
         <div className="ui simple dropdown icon item">
            <i className="wrench icon"></i>
            <div className="menu">
               { dropdownItemNodes }
            </div>
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
