import React from 'react';
import Remarkable from 'remarkable';

class Text extends React.Component {
  render() {
    const md = new Remarkable();
    const rawMarkup = md.render(this.props.data.text);
    return <span dangerouslySetInnerHTML={{ __html: rawMarkup }} />;
  }
}

module.exports = Text;