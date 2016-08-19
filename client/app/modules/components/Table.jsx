import React from 'react';
import { Table as BootstrapTable } from 'react-bootstrap';


class Table extends React.Component {
  render() {
    const headerNodes = this.props.data.headers.map((header, i) => {
      return <th key={i}>{header}</th>;
    });
    const bodyNodes = this.props.data.rows.map((row, i) => {
      const itemNodes = row.map((item, j) => {
        return <td key={j}>{item}</td>;
      });
      return <tr key={i}>{itemNodes}</tr>;
    });

    return (
      <BootstrapTable bordered condensed hover>
        <thead>
          <tr>
            {headerNodes}
          </tr>
        </thead>
        <tbody>
          {bodyNodes}
        </tbody>
      </BootstrapTable>
    );
  }
}

module.exports = Table;