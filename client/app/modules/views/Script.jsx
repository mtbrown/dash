import React from 'react';


import { Content } from './Content.jsx';
import { Grid } from './Grid.jsx';

import { get } from '../utils/api.js';

export class Script extends React.Component {
  constructor() {
    super();
    this.state = {loading: true, grid: {}};
    this.fetchGrid = this.fetchGrid.bind(this);
  }

  async fetchGrid() {
    if(this.ignoreLastFetch) {
      return;
    }
    const response = await get(`/api/scripts/${this.props.params.scriptId}/grid`);
    this.setState({loading: false, grid: response});
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
    var content;
    if (this.state.loading) {
      content = <span>Loading...</span>;
    } else {
      content = <Grid grid={this.state.grid} script_id={this.props.params.scriptId} />;
    }

    return (
      <Content title="Script">
        {content}
      </Content>
    );
  }
}
