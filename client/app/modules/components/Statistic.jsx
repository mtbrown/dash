import React from 'react';


class Statistic extends React.Component {
  render() {
    const text = String(this.props.data.value) + " " + this.props.data.unit;
    return (
      <div className="panel panel-primary">
        <div className="panel-heading">
          <div className="row">
            <div className="col-xs-3">
              <i className="fa fa-comments fa-5x"></i>
            </div>
            <div className="col-xs-9 text-right">
              <div className="huge">{text}</div>
              <div>{this.props.data.description}</div>
            </div>
          </div>
        </div>
        <a href="#">
          <div className="panel-footer">
            <span className="pull-left">View Details</span>
            <span className="pull-right"><i className="fa fa-arrow-circle-right"></i></span>
            <div className="clearfix"></div>
          </div>
        </a>
      </div>
    );
  }
}

module.exports = Statistic;