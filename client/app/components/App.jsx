import React from 'react';

import {Navigation} from './Navigation/Navigation.jsx';
import {Content} from './Content.jsx';


export class App extends React.Component {
  render() {
    return (
      <div>
        <Navigation />
        <Content />
      </div>
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
          <Content />
        </div>
      </div>
    );
  }
}
