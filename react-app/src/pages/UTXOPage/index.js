import React, { Component } from "react";
import Button from 'react-bootstrap/Button';
import Collapse from 'react-bootstrap/Collapse';

import './index.css';
import DetailedUTXOCard from "../../components/DetailedUTXOCard";

class UTXOPage extends Component {
  state = {
    utxos: [],
    title: '',
    open: false
  };

  get_my_utxos = () => {
    fetch('/myUnspentTransactionOutputs', {method: "GET"})
      .then((res) => res.json()).then((data) => {
        let utxos = data.map((utxo) => JSON.parse(utxo));
        this.setState({utxos});
    });
  };

  get_all_utxos = () => {
    fetch('/unspentTransactionOutputs', {method: "GET"})
      .then((res) => res.json()).then((data) => {
        let utxos = data.map((utxo) => JSON.parse(utxo));
        this.setState({utxos});
    });
  }

  set_open = (open) => {
    this.setState({open});
  }

  componentDidMount = () => {
    let func = this.props.type === 'MY' ? this.get_my_utxos : this.get_all_utxos;
    let title = this.props.type === 'MY' ? 'MY UTXOs' : 'All UTXOs';
    this.setState({title});
    func();
    this.interval = setInterval(() => {
      func();
    }, 10000);
  };

  componentWillUnmount = () => {
    clearInterval(this.interval);
  };

  render() {
    return (
      <>
        <h1>{this.state.title}</h1>
        <Button
          onClick={() => this.set_open(!this.state.open)}
          aria-controls="example-collapse-text"
          aria-expanded={this.state.open}
        >
          Click to Show/Hide
        </Button>
        <Collapse in={this.state.open} >
          <div className="utxos">
            {this.state.utxos.map((utxo) => {
              return (
                <DetailedUTXOCard utxo={utxo} />
              );
            })}
          </div>
        </Collapse>
        {this.state.utxos.length === 0 && <p>No UTXOs to display.</p>}
      </>
    )
  }

}

export default UTXOPage;