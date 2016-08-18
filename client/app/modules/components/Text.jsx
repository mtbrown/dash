import React from 'react';

class Text extends React.Component {
  render() {
    return <span>{this.props.data.text}</span>;
  }
}

module.exports = Text;