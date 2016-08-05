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
            <SidebarSearch />
            <SidebarMenuItem icon="fa-dashboard" text="Dashboard" href="/" />
            <SidebarMenuItem icon="fa-server" text="System" href="/system/" />
            <ScriptListMenu scriptList={scriptList} />
          </ul>
        </div>
      </div>
    );
  }
}


class SidebarSearch extends React.Component {
  render() {
    return (
      <li className="sidebar-search">
        <div className="input-group custom-search-form">
          <input
            type="text"
            className="form-control"
            placeholder="Search...">
          </input>
          <span className="input-group-btn">
            <button className="btn btn-default" type="button">
              <i className="fa fa-search">
              </i>
            </button>
          </span>
        </div>
      </li>
    );
  }
}


class SidebarMenuItem extends React.Component {
  render() {
    let iconClass = classNames('fa', this.props.icon, 'fa-fw');
    return (
      <li>
        <a href={this.props.href}>
          <i className={iconClass}></i>
          {this.props.text}
        </a>
      </li>
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
          href={'/scripts/' + script.id + '/'}
          text={script.title}
          key={script.id}
        />
      );
    });

    return (
      <div className="list-group">
        {scriptItemNodes}
      </div>
    );
  }
}


class ScriptListItem extends React.Component {
  render() {
    var itemClass = classNames('list-group-item', {'active': this.props.active});
    var labelClass = classNames('ui', this.props.color,
      {'left pointing': this.props.active}, 'label');

    return (
      <a href={this.props.href} className={itemClass}>
        {this.props.text}
      </a>
    );
  }
}
