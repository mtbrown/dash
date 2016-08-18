import React from 'react';
import { get } from '../utils/api.js';
import { socket } from '../App.jsx';


const componentMap = {
  Text: React.createFactory(require('./Text.jsx'))
};


export class Component extends React.Component {
  constructor() {
    super();
    this.state = {};
    this.handleChange = this.handleChange.bind(this);
  }

  async componentDidMount() {
    const response = await get(`/api/components/${this.props.id}`);
    this.setState(response);

    socket.on(this.props.id, (data) => {
      this.handleChange(data);
    });

    socket.emit('join', {room: this.props.id});
  }

  componentWillUnmount() {
    socket.emit('leave', {room: this.props.id});
  }

  handleChange(newState) {
    console.log(`id: ${this.props.id}, newState: ${newState}`);
    this.setState(newState);
  }

  render() {
    return <ComponentView id={this.props.id} type={this.props.type} data={this.state} />;
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