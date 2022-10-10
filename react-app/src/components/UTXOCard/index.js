import React, { Component } from "react";
import Card from 'react-bootstrap/Card';

import './index.css';

class UTXOCard extends Component {
  constructor(props) {
    super(props);
    this.state = {
      type: 0,
      address: '',
      amount: 0,
      is_coinbase: false
    };
  };

  get_tx = (id, index) => {
    fetch(`/transaction/${id}`, {method: "GET"}
    ).then((res) => res.json()).then((tx) => {
      let tx_out = tx.tx_outs[index];
      this.setState({ address: tx_out.address, amount: tx_out.amount, is_coinbase: false });
    }).catch((err) => {
      console.log(err);
    });
  };

  componentDidMount = () => {
    if (this.props.tx_out) {
      let tx_out = this.props.tx_out;
      this.setState({ address: tx_out.address, amount: tx_out.amount, is_coinbase: false });
    } else if (this.props.tx_in) {
      let tx_in = this.props.tx_in;
      if (tx_in.tx_out_id === '' && tx_in.tx_out_index === 0 && tx_in.signature === '') {
        this.setState({is_coinbase: true})
      } else {
        this.get_tx(tx_in.tx_out_id, tx_in.tx_out_index);
      }
    }
  };

  render() {
    return(
      <Card className="utxo_card">
        <Card.Body>
          {this.state.address && <Card.Link>{this.state.address}</Card.Link>}
          {!this.state.is_coinbase && <p>Amount: {this.state.amount}</p>}
          {this.state.is_coinbase && <p>Coinbase</p>}
        </Card.Body>
      </Card>
    )
  };

}

export default UTXOCard;