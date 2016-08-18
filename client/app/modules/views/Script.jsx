import React from 'react';
import { Grid, Row, Col } from 'react-bootstrap';

import { Content } from './Content.jsx';
import { Component } from '../components/Component.jsx';
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
        <ScriptView grid={this.state.grid} />
      </Content>
    );
  }
}


class ScriptView extends React.Component {
  render() {
    const columnSize = 12 / this.props.grid.columns.length;

    const scriptComponents = this.props.grid.columns.map((column, i) => {
      return (
        <Col md={columnSize} key={i}>
          {column.map((component) => {
            return (
              <Row key={component.id}>
                <Component id={component.id} type={component.type} key={component.id} />
              </Row>
            );
          })}
        </Col>
      );
    });

    return (
      <Grid>
        <Row>
          {scriptComponents}
        </Row>
      </Grid>
    )
  }
}