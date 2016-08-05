import React from 'react';
import classNames from 'classnames';

var scriptList = [
  {id: "thermometer", title: "Thermometer", status: "ok", notificationCount: 8},
  {id: "podcasts", title: "Podcasts", status: "ok", notificationCount: 0},
  {id: "yt_archive", title: "YouTube Archive", status: "ok", notificationCount: 3},
  {id: "test", title: "Test", status: "error", notificationCount: 7},
  {id: "wow", title: "Wow", status: "ok", notificationCount: 12}
];


export class Sidebar extends React.Component {
  render() {
    return (
      <div className="navbar-default sidebar" role="navigation">
        <div className="sidebar-nav navbar-collapse">
          <ul className="nav" id="side-menu">


              <div className="list-group">
                <a href="#" className="list-group-item active">
                  Cras justo odio
                </a>
                <a href="#" className="list-group-item">Dapibus ac facilisis in</a>
                <a href="#" className="list-group-item">Morbi leo risus</a>
                <a href="#" className="list-group-item">Porta ac consectetur ac</a>
                <a href="#" className="list-group-item">Vestibulum at eros</a>
              </div>


            <li className="sidebar-search">
              <div className="input-group custom-search-form">
                <input type="text" className="form-control" placeholder="Search..."></input>
            <span className="input-group-btn">
                              <button className="btn btn-default" type="button">
                                  <i className="fa fa-search"></i>
                              </button>
                          </span>
              </div>
            </li>
            <li>
              <a href="index.html"><i className="fa fa-dashboard fa-fw"></i> Dashboard</a>
            </li>
            <li>
              <a href="#"><i className="fa fa-bar-chart-o fa-fw"></i> Charts<span className="fa arrow"></span></a>
              <ul className="nav nav-second-level">
                <li>
                  <a href="flot.html">Flot Charts</a>
                </li>
                <li>
                  <a href="morris.html">Morris.js Charts</a>
                </li>
              </ul>
            </li>
            <li>
              <a href="tables.html"><i className="fa fa-table fa-fw"></i> Tables</a>
            </li>
            <li>
              <a href="forms.html"><i className="fa fa-edit fa-fw"></i> Forms</a>
            </li>
            <li>
              <a href="#"><i className="fa fa-wrench fa-fw"></i> UI Elements<span className="fa arrow"></span></a>
              <ul className="nav nav-second-level">
                <li>
                  <a href="panels-wells.html">Panels and Wells</a>
                </li>
                <li>
                  <a href="buttons.html">Buttons</a>
                </li>
                <li>
                  <a href="notifications.html">Notifications</a>
                </li>
                <li>
                  <a href="typography.html">Typography</a>
                </li>
                <li>
                  <a href="icons.html"> Icons</a>
                </li>
                <li>
                  <a href="grid.html">Grid</a>
                </li>
              </ul>
            </li>
            <li>
              <a href="#"><i className="fa fa-sitemap fa-fw"></i> Multi-Level Dropdown<span className="fa arrow"></span></a>
              <ul className="nav nav-second-level">
                <li>
                  <a href="#">Second Level Item</a>
                </li>
                <li>
                  <a href="#">Second Level Item</a>
                </li>
                <li>
                  <a href="#">Third Level <span className="fa arrow"></span></a>
                  <ul className="nav nav-third-level">
                    <li>
                      <a href="#">Third Level Item</a>
                    </li>
                    <li>
                      <a href="#">Third Level Item</a>
                    </li>
                    <li>
                      <a href="#">Third Level Item</a>
                    </li>
                    <li>
                      <a href="#">Third Level Item</a>
                    </li>
                  </ul>
                </li>
              </ul>
            </li>
            <li>
              <a href="#"><i className="fa fa-files-o fa-fw"></i> Sample Pages<span className="fa arrow"></span></a>
              <ul className="nav nav-second-level">
                <li>
                  <a href="blank.html">Blank Page</a>
                </li>
                <li>
                  <a href="login.html">Login Page</a>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    );
  }
}


class SidebarTitle extends React.Component {
  render() {
    return (
      <div className="item">
        <a href="/">
          <h2>Dash</h2>
        </a>
      </div>
    );
  }
}


class ScriptListMenu extends React.Component {
  render() {
    var scriptItemNodes = this.props.scriptList.map(function (script) {
      return (
        <ScriptListItem
          active={false}
          label={script.notificationCount}
          color={script.status == "ok" ? 'teal' : 'red'}
          url={'/scripts/' + script.id + '/'}
          text={script.title}
          key={script.id}
        />
      );
    });

    return (
      <div className="item">
        <h3>Scripts</h3>
        <div className="menu">
          { scriptItemNodes }
        </div>
      </div>
    );
  }
}


class ScriptListItem extends React.Component {
  render() {
    var itemClass = classNames({'active': this.props.active}, 'item');
    var labelClass = classNames('ui', this.props.color,
      {'left pointing': this.props.active}, 'label');

    return (
      <a className={itemClass} href={this.props.url}>
        {this.props.text}
        <div className={labelClass}>{this.props.label}</div>
      </a>
    );
  }
}
