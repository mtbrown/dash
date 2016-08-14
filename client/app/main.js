import React from 'react';
import ReactDOM from 'react-dom';

import { Router, browserHistory } from 'react-router';

import { App } from './modules/App.jsx';
import { Dashboard  } from './modules/views/Dashboard.jsx';
import { Settings } from './modules/views/Settings.jsx';
import { System } from './modules/views/System.jsx';
import { Script } from './modules/views/Script.jsx';

const routes = {
  path: '/',
  component: App,
  indexRoute: {component: Dashboard},
  childRoutes: [
    {path: '/settings', component: Settings},
    {path: '/system', component: System},
    {path: '/scripts/:scriptId', component: Script}
  ]
};

ReactDOM.render(
  <Router history={browserHistory} routes={routes} />,
  document.getElementById('container')
);


$(function() {
  $('#side-menu').metisMenu();
});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
  $(window).bind("load resize", function() {
    var topOffset = 50;
    var width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
    if (width < 768) {
      $('div.navbar-collapse').addClass('collapse');
      topOffset = 100; // 2-row-menu
    } else {
      $('div.navbar-collapse').removeClass('collapse');
    }

    var height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
    height = height - topOffset;
    if (height < 1) height = 1;
    if (height > topOffset) {
      $("#page-wrapper").css("min-height", (height) + "px");
    }
  });
});
