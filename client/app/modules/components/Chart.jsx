import React from 'react';
import { Line, Bar,  } from 'react-chartjs';

const chartTypeMap = {
  LineChart: React.createFactory(Line),
  BarChart: React.createFactory(Bar)
};

class Chart extends React.Component {
  render() {
    return chartTypeMap[this.props.type]({
      data: this.props.data.data,
      options: this.props.data.options,
      ref: (ref) => {
        this.chart = ref;
      }
    });
  }
}

module.exports = Chart;