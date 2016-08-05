import React from 'react';


export class Navbar extends React.Component {
  render() {
    return (
      <div>
        <div className="navbar-header">
          <button type="button" className="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span className="sr-only">Toggle navigation</span>
            <span className="icon-bar"></span>
            <span className="icon-bar"></span>
            <span className="icon-bar"></span>
          </button>
          <a className="navbar-brand" href="index.html">Dash</a>
        </div>

        <ul className="nav navbar-top-links navbar-right">
          <li className="dropdown">
            <a className="dropdown-toggle" data-toggle="dropdown" href="#">
              <i className="fa fa-envelope fa-fw"></i>  <i className="fa fa-caret-down"></i>
            </a>
            <ul className="dropdown-menu dropdown-messages">
              <li>
                <a href="#">
                  <div>
                    <strong>John Smith</strong>
                    <span className="pull-right text-muted">
                                        <em>Yesterday</em>
                                    </span>
                  </div>
                  <div>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eleifend...</div>
                </a>
              </li>
              <li className="divider"></li>
              <li>
                <a href="#">
                  <div>
                    <strong>John Smith</strong>
                    <span className="pull-right text-muted">
                                        <em>Yesterday</em>
                                    </span>
                  </div>
                  <div>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eleifend...</div>
                </a>
              </li>
              <li className="divider"></li>
              <li>
                <a href="#">
                  <div>
                    <strong>John Smith</strong>
                    <span className="pull-right text-muted">
                                        <em>Yesterday</em>
                                    </span>
                  </div>
                  <div>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eleifend...</div>
                </a>
              </li>
              <li className="divider"></li>
              <li>
                <a className="text-center" href="#">
                  <strong>Read All Messages</strong>
                  <i className="fa fa-angle-right"></i>
                </a>
              </li>
            </ul>
          </li>
          <li className="dropdown">
            <a className="dropdown-toggle" data-toggle="dropdown" href="#">
              <i className="fa fa-tasks fa-fw"></i>  <i className="fa fa-caret-down"></i>
            </a>
          </li>
          <li className="dropdown">
            <a className="dropdown-toggle" data-toggle="dropdown" href="#">
              <i className="fa fa-bell fa-fw"></i>  <i className="fa fa-caret-down"></i>
            </a>
            <ul className="dropdown-menu dropdown-alerts">
              <li>
                <a href="#">
                  <div>
                    <i className="fa fa-comment fa-fw"></i> New Comment
                    <span className="pull-right text-muted small">4 minutes ago</span>
                  </div>
                </a>
              </li>
              <li className="divider"></li>
              <li>
                <a href="#">
                  <div>
                    <i className="fa fa-twitter fa-fw"></i> 3 New Followers
                    <span className="pull-right text-muted small">12 minutes ago</span>
                  </div>
                </a>
              </li>
              <li className="divider"></li>
              <li>
                <a href="#">
                  <div>
                    <i className="fa fa-envelope fa-fw"></i> Message Sent
                    <span className="pull-right text-muted small">4 minutes ago</span>
                  </div>
                </a>
              </li>
              <li className="divider"></li>
              <li>
                <a href="#">
                  <div>
                    <i className="fa fa-tasks fa-fw"></i> New Task
                    <span className="pull-right text-muted small">4 minutes ago</span>
                  </div>
                </a>
              </li>
              <li className="divider"></li>
              <li>
                <a href="#">
                  <div>
                    <i className="fa fa-upload fa-fw"></i> Server Rebooted
                    <span className="pull-right text-muted small">4 minutes ago</span>
                  </div>
                </a>
              </li>
              <li className="divider"></li>
              <li>
                <a className="text-center" href="#">
                  <strong>See All Alerts</strong>
                  <i className="fa fa-angle-right"></i>
                </a>
              </li>
            </ul>
          </li>
          <li className="dropdown">
            <a className="dropdown-toggle" data-toggle="dropdown" href="#">
              <i className="fa fa-user fa-fw"></i>  <i className="fa fa-caret-down"></i>
            </a>
            <ul className="dropdown-menu dropdown-user">
              <li><a href="#"><i className="fa fa-user fa-fw"></i> User Profile</a>
              </li>
              <li><a href="#"><i className="fa fa-gear fa-fw"></i> Settings</a>
              </li>
              <li className="divider"></li>
              <li><a href="login.html"><i className="fa fa-sign-out fa-fw"></i> Logout</a>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    );
  }
}
