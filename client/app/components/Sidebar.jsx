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
         <div className="ui large left vertical visible menu inverted sidebar">
            <SidebarTitle />
            <ScriptListMenu scriptList={scriptList} />
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
      var scriptItemNodes = this.props.scriptList.map(function(script) {
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
