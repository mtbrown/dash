import React from 'react';
import ReactDOM from 'react-dom';

import { Router, browserHistory } from 'react-router';

import { App } from './components/App.jsx';
import { Dashboard  } from './components/Views/Dashboard.jsx';
import { Settings } from './components/Views/Settings.jsx';
import { System } from './components/Views/System.jsx';

const routes = {
  path: '/',
  component: App,
  indexRoute: {component: Dashboard},
  childRoutes: [
    {path: 'settings', component: Settings},
    {path: 'system', component: System}
  ]
};

ReactDOM.render(
  <Router history={browserHistory} routes={routes} />,
  document.getElementById('container')
);
