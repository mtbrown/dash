import React from 'react';

import { Content } from './Content.jsx';


export class Script extends React.Component {
  render() {
    return (
      <Content title="Script">
        {this.props.params.scriptId}
      </Content>
    );
  }
}