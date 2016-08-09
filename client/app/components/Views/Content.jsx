import React from 'react';


export class Content extends React.Component {
  render() {
    return (
      <div id="page-wrapper">
        <div className="row">
          <div className="col-lg-12">
            <h1 className="page-header">{this.props.title}</h1>
          </div>
        </div>
      </div>
    );
  }
}
