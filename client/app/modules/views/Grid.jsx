import React from 'react';

import { Component } from '../components/Component.jsx';
import { Grid as BootstrapGrid, Row, Col } from 'react-bootstrap';


export class Grid extends React.Component {
  constructor() {
    super();

    this.renderRecursive = this.renderRecursive.bind(this);
  }

  renderRecursive(element) {
    if (element instanceof Array) {
      return element.map(this.renderRecursive);
    }
    if (element.type != "Row" && element.type != "Col") {
      console.log(element);
      console.log(`Component: type=${element.type}, id=${element.id}`);
      return <Component id={element.id} type={element.type} key={element.id} />;
    }

    const children = element.children.map(this.renderRecursive);
    if (element.type == 'Row') {
      return <Row>{children}</Row>;
    }
    if (element.type == 'Col') {
      element.props.children = element.children;
      return React.createFactory(Col)(element.props);
    }
  }

  render() {
    const children = this.renderRecursive(this.props.grid);

    return (
      <BootstrapGrid fluid={true}>
        {children}
      </BootstrapGrid>
    );
  }
}