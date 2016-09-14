import React from 'react';

import { Component } from '../components/Component.jsx';
import { Grid as BootstrapGrid, Row, Col } from 'react-bootstrap';


export class Grid extends React.Component {
  constructor() {
    super();
    this.renderRecursive = this.renderRecursive.bind(this);
  }

  renderRecursive(element, index) {
    if (element.type != "Row" && element.type != "Col" && element.type != "Grid") {
      return <Component
        id={element.id}
        type={element.type}
        scriptId={this.props.scriptId}
        key={element.id}
      />;
    }

    const children = element.children.map(this.renderRecursive);
    if (element.type == 'Grid') {
      return <BootstrapGrid fluid={true}>{children}</BootstrapGrid>;
    }
    if (element.type == 'Row') {
      return <Row key={index}>{children}</Row>;
    }
    if (element.type == 'Col') {
      const props = element.props;
      props.key = index;
      props.children = children;
      return React.createFactory(Col)(props);
    }
  }

  render() {
    return this.renderRecursive(this.props.grid, 0);
  }
}