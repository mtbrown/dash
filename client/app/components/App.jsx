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
