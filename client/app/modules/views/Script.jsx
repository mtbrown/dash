import React from 'react';

import { Content } from './Content.jsx';
import { socket } from '../App.jsx';
import { get } from '../utils/api.js';

export class Script extends React.Component {
  constructor() {
    super();
    this.state = {grid: {columns: []}};
    this.fetchGrid = this.fetchGrid.bind(this);
  }

  async fetchGrid() {
    if(this.ignoreLastFetch) {
      return;
    }
    const response = await get(`/api/scripts/${this.props.params.scriptId}/grid`);
    this.setState({grid: response});
    console.log("grid: " + response)
  }

  componentDidMount() {
    this.fetchGrid();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.params.scriptId != this.props.params.scriptId) {
      this.fetchGrid();
    }
  }

  componentWillUnmount() {
    this.ignoreLastFetch = true;
  }

  render() {
    return (
      <Content title="Script">
        {this.props.params.scriptId}
      </Content>
    );
  }
}


class ScriptView extends React.Component {

}