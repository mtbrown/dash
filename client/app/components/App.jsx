import React from 'react';

import { Sidebar } from './Sidebar.jsx';
import { Grid } from './Grid.jsx';


export class App extends React.Component {
   render() {
      return (
         <SidebarWrapper />
      );
   }
}


class SidebarWrapper extends React.Component {
   render() {
      return (
         <div>
            <div className="ui large left vertical visible menu inverted sidebar">
               <Sidebar />
            </div>
            <div className="pusher">
               <Grid />
            </div>
         </div>
      );
   }
}
