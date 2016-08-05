import React from 'react';


export class Content extends React.Component {
  render() {
    return (
      <div id="page-wrapper">
        <div className="row">
          <div className="col-lg-12">
            <h1 className="page-header">Dashboard</h1>
          </div>
        </div>
      </div>
    );
  }
}


class ContentTitle extends React.Component {
  render() {
    return (
      <h1 className="ui dividing header">Hello</h1>



    );
  }
}