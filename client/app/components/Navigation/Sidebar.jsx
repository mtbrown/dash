import React from 'react';
import classNames from 'classnames'
import { Link, IndexLink } from 'react-router';

var scriptList = [
  {id: "thermometer", title: "Thermometer", status: "ok", notificationCount: 8},
  {id: "podcasts", title: "Podcasts", status: "ok", notificationCount: 0},
  {id: "yt_archive", title: "YouTube Archive", status: "warning", notificationCount: 3},
  {id: "test", title: "Test", status: "error", notificationCount: 7},
  {id: "wow", title: "Wow", status: "ok", notificationCount: 1204}
];


const statusColorMap = {ok: "primary", warning: "warning", error: "danger"};


export class Sidebar extends React.Component {
  render() {
    return (
      <div className="navbar-default sidebar" role="navigation">
        <div className="sidebar-nav navbar-collapse">
          <ul className="nav" id="side-menu">
            <SidebarSearch />
            <SidebarMenuItem icon="fa-dashboard" text="Dashboard" link="/" />
            <SidebarMenuItem icon="fa-server" text="System" link="/system" />
            <SidebarMenuItem icon="fa-cogs" text="Settings" link="/settings" />
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
        <IndexLink to={this.props.link} activeClassName="active">
          <i className={iconClass} style={{margin: 5}}></i>
          {this.props.text}
        </IndexLink>
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
          status={script.status}
          href={'/scripts/' + script.id + '/'}
          text={script.title}
          key={script.id}
        />
      );
    });

    return (
      <div className="list-group" style={{margin: 15}}>
        {scriptItemNodes}
      </div>
    );
  }
}


class ScriptListItem extends React.Component {
  render() {
    var itemClass = classNames('list-group-item', {'active': this.props.active}, 'small');
    var labelClass = classNames('pull-right', 'label', 'label-' + statusColorMap[this.props.status]);

    return (
      <a href={this.props.href} className={itemClass}>
        {this.props.text}
        <span className={labelClass} style={{fontSize: "90%"}}>{this.props.label}</span>
      </a>
    );
  }
}
