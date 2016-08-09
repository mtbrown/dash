import React from 'react';

import {Navigation} from './Navigation/Navigation.jsx';
import {Content} from './Views/Content.jsx';


export class App extends React.Component {
  render() {
    return (
      <div>
        <Navigation />
        {this.props.children}
      </div>
    );
  }
}
