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


