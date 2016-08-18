import React from 'react';
import { get } from '../utils/api.js';
import { socket } from '../App.jsx';


const componentMap = {
  Text: React.createFactory(require('./Text.jsx'))
};


export class Component extends React.Component {
  constructor() {
    super();
    this.state = {data: {}};
    this.dataHandler = this.dataHandler.bind(this);
  }

  async componentDidMount() {
    const response = await get(`/api/components/${this.props.id}`);
    this.dataHandler(response);
    socket.on(this.props.id, this.dataHandler);
    socket.emit('join', {room: this.props.id});
  }

  componentWillUnmount() {
    socket.emit('leave', {room: this.props.id});
    socket.removeListener(this.props.id, this.dataHandler);
  }

  dataHandler(newData) {
    this.setState({data: newData});
  }

  render() {
    return <ComponentView id={this.props.id} type={this.props.type} data={this.state.data} />;
  }
}


class ComponentView extends React.Component {
  render() {
    return componentMap[this.props.type]({
      id: this.props.id,
      data: this.props.data
    });
  }
}