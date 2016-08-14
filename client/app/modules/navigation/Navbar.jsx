import React from 'react';
import classNames from 'classnames';

export class Navbar extends React.Component {
  render() {
    return (
      <div>
        <NavbarHeader />

        <ul className="nav navbar-top-links navbar-right">
          <NavbarDropdown icon="fa-envelope" className="dropdown-messages">
            <DropdownMessage
              author="John Smith"
              time="Yesterday"
              message="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
            />
            <DropdownDivider />
            <DropdownMessage
              author="John Smith"
              time="Yesterday"
              message="Lorem ipsum dolor sit amet, consectetur adipiscing elit."
            />
            <DropdownDivider />
            <DropdownAction text="Read All Messages" />
          </NavbarDropdown>

          <NavbarDropdown icon="fa-tasks" className="dropdown-tasks" />

          <NavbarDropdown icon="fa-bell" className="dropdown-alerts">
            <DropdownAlert icon="fa-comment" text="New Comment" time="4 minutes ago" />
            <DropdownDivider />
            <DropdownAlert icon="fa-twitter" text="3 New Followers" time="12 minutes ago" />
            <DropdownDivider />
            <DropdownAlert icon="fa-envelope" text="Message Sent" time="18 minutes ago" />
            <DropdownDivider />
            <DropdownAction text="See All Alerts" />
          </NavbarDropdown>

          <NavbarUserMenu />
        </ul>
      </div>
    );
  }
}


class NavbarHeader extends React.Component {
  render() {
    return (
      <div className="navbar-header">
        <button type="button" className="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
          <span className="sr-only">Toggle navigation</span>
          <span className="icon-bar"></span>
          <span className="icon-bar"></span>
          <span className="icon-bar"></span>
        </button>
        <a className="navbar-brand" href="index.html">Dash</a>
      </div>
    );
  }
}


class NavbarUserMenu extends React.Component {
  render() {
    return (
      <NavbarDropdown icon="fa-user" className="dropdown-user">
        <li><a href="#"><i className="fa fa-user fa-fw"></i> User Profile</a>
        </li>
        <li><a href="#"><i className="fa fa-gear fa-fw"></i> Settings</a>
        </li>
        <li className="divider"></li>
        <li><a href="login.html"><i className="fa fa-sign-out fa-fw"></i> Logout</a>
        </li>
      </NavbarDropdown>
    );
  }
}


class NavbarDropdown extends React.Component {
  render() {
    let iconClass = classNames('fa', this.props.icon, 'fa-fw');
    let dropdownClass = classNames('dropdown-menu', this.props.className);
    return (
      <li className="dropdown">
        <a className="dropdown-toggle" data-toggle="dropdown" href="#">
          <i className={iconClass}></i>  <i className="fa fa-caret-down"></i>
        </a>
        <ul className={dropdownClass}>
          {this.props.children}
        </ul>
      </li>
    );
  }
}


class DropdownDivider extends React.Component {
  render() {
    return <li className="divider"></li>;
  }
}


class DropdownAction extends React.Component {
  render() {
    return (
      <li>
        <a className="text-center" href="#">
          <strong>{this.props.text}</strong>
          <i className="fa fa-angle-right"></i>
        </a>
      </li>
    );
  }
}


class DropdownMessage extends React.Component {
  render() {
    return (
      <li>
        <a href="#">
          <div>
            <strong>{this.props.author}</strong>
            <span className="pull-right text-muted">
              <em>{this.props.time}</em>
            </span>
          </div>
          <div>{this.props.message}</div>
        </a>
      </li>
    );
  }
}


class DropdownAlert extends React.Component {
  render() {
    let iconClass = classNames('fa', this.props.icon, 'fa-fw');
    return (
      <li>
        <a href="#">
          <div>
            <i className={iconClass}></i> {this.props.text}
            <span className="pull-right text-muted small">{this.props.time}</span>
          </div>
        </a>
      </li>
    );
  }
}
