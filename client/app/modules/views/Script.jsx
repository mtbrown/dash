import React from 'react';

import { Content } from './Content.jsx';
import { socket } from '../App.jsx';

export class Script extends React.Component {
  constructor() {
    super();
    this.state = {scripts: {}};
    console.log("constructor");

    socket.on("scriptGrid", (message) => {
      if (message.status != "success") {
        console.log(message.response.message);
        return;
      }
      this.setState({scripts: this.state.scripts})
    })
  }

  componentDidMount() {
    console.log("componentDidMount");
  }

  render() {
    return (
      <Content title="Script">
        {this.props.params.scriptId}
      </Content>
    );
  }
}