import React from 'react';
import { ProgressBar as BootstrapProgressBar } from 'react-bootstrap';


class ProgressBar extends React.Component {
  render() {
    const label = this.props.data.label ? `${this.props.data.value}%` : '';
    return (
      <BootstrapProgressBar
        active={this.props.data.animated}
        bsStyle={this.props.data.style}
        label={label}
        now={this.props.data.value}
        striped={this.props.data.striped}
      />
    );
  }
}

module.exports = ProgressBar;