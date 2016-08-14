import React from 'react';
import io from 'socket.io-client';

import {Navigation} from './navigation/Navigation.jsx';

export const socket = io.connect('/api');

export class App extends React.Component {
  constructor() {
    super();
    socket.on('connect', () => {
      console.log("Connected successfully!");
    })
  }

  render() {
    return (
      <div>
        <Navigation />
        {this.props.children}
      </div>
    );
  }
}
