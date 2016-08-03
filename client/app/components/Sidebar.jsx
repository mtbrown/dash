import React from 'react';

export class Sidebar extends React.Component {
   render() {
      return (
         <div className="ui vertical menu">
            <a className="active teal item">
               Inbox
               <div className="ui teal left pointing label">1</div>
            </a>
            <a className="item">
               Spam
               <div className="ui label">51</div>
            </a>
            <a className="item">
               Updates
               <div className="ui label">1</div>
            </a>
         </div>
      );
   }
}

class SidebarItem extends React.Component {
   render() {
      return (
         <a className="active teal item">
            Inbox
            <div className="ui teal left pointing label">1</div>
         </a>
      );
   }
}