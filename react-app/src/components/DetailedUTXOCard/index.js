import React, { Component } from "react";
import Card from 'react-bootstrap/Card';

class DetailedUTXOCard extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return(
      <Card style={{'width': '250px'}}>
        <Card.Body>
          <p>TxOut ID: {this.props.utxo.tx_out_id}</p>
          <p>TxOut Index: {this.props.utxo.tx_out_index}</p>
          <p>Address: {this.props.utxo.address}</p>
          <p>Amount: {this.props.utxo.amount}</p>
        </Card.Body>
      </Card>
    );
  };

}

export default DetailedUTXOCard;