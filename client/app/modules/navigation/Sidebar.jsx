import React from 'react';
import classNames from 'classnames'
import { Link, IndexLink } from 'react-router';

import { socket } from '../App.jsx';
import { get } from '../utils/api.js';


const statusColorMap = {ok: "info", warning: "warning", error: "danger"};


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
            <ScriptListMenu />
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
  constructor(props) {
    super(props);
    this.state = {scriptList: []};
  }

  async componentWillMount() {
    const scriptList = await get('/api/scripts');
    this.setState({scriptList: scriptList})
  }

  render() {
    return <ScriptList scriptList={this.state.scriptList} />
  }
}


class ScriptList extends React.Component {
  render() {
    var scriptItemNodes = this.props.scriptList.map(function (script) {
      return (
        <ScriptListItem
          label={script.label}
          status={script.status}
          href={'/scripts/' + script.id}
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
    var labelClass = classNames('pull-right', 'label', 'label-' + statusColorMap[this.props.status]);

    return (
      <Link to={this.props.href} className="list-group-item small" activeClassName="list-group-item active small">
        {this.props.text}
        <span className={labelClass} style={{fontSize: "90%"}}>{this.props.label}</span>
      </Link>
    );
  }
}
